
import html
import re
import requests
import streamlit as st

API_URL = "https://sourcechat-ajmal.onrender.com"


def clean_url(url):
    if not isinstance(url, str):
        return ""

    match = re.search(r"https?://[^\s\])]+", url)

    if match:
        return match.group(0).rstrip(".")

    if url.startswith(("https://", "http://")):
        return url

    return ""


def show_verification_report(data):

    report = data.get("verification_report", {})
    risk = report.get("risk_assessment", {})

    # All these fields are nested inside risk_assessment
    license_info = risk.get("license_assessment", {})
    scope_assessment = risk.get("license_scope_assessment", [])
    source_assessment = risk.get("source_assessment", [])
    recommendations = risk.get("recommendations", [])
    limitations = risk.get("limitations", [])

    # External sources are directly inside verification_report
    external_sources = report.get("external_sources", [])

    risk_level = risk.get("risk_level", "UNKNOWN").upper()

    st.markdown("---")
    st.markdown("## 🛡️ Verification Results")

    if risk_level == "LOW":
        st.success(f"Risk Level: {risk_level}")
    elif risk_level == "MEDIUM":
        st.warning(f"Risk Level: {risk_level}")
    elif risk_level == "HIGH":
        st.error(f"Risk Level: {risk_level}")
    else:
        st.info(f"Risk Level: {risk_level}")

    st.info(risk.get("summary", "No summary available."))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Pages",
            report.get("total_pages", 0)
        )

    with col2:
        st.metric(
            "Evidence Found",
            report.get("total_evidence", 0)
        )

    with col3:
        st.metric(
            "External Sources",
            len(external_sources)
        )

    with st.expander("📄 Document Information", expanded=True):
        st.write("**Filename:**", data.get("filename", "Unknown"))
        st.write("**Session ID:**", data.get("session_id", "N/A"))
        st.write("**Document ID:**", data.get("document_id", "N/A"))

    # COPYRIGHT AND LICENSE ASSESSMENT

    st.markdown("---")
    st.markdown("### ©️ Copyright & License Assessment")

    identified_licenses = license_info.get(
        "identified_licenses", []
    )

    ownership = license_info.get(
        "ownership_findings", []
    )

    concerns = license_info.get(
        "concerns", []
    )

    if identified_licenses:
        st.markdown("**Identified Licenses**")

        for item in identified_licenses:
            st.write(f"- {item}")
    else:
        st.info("No specific license identified.")

    if ownership:
        st.markdown("**Ownership Findings**")

        for item in ownership:
            st.write(f"- {item}")

    if concerns:
        st.warning("**License Concerns**")

        for item in concerns:
            st.write(f"- {item}")
    else:
        st.success("No specific license concerns reported.")

    # LICENSE SCOPE

    if scope_assessment:

        st.markdown("#### License Scope Assessment")

        for index, item in enumerate(scope_assessment, 1):

            with st.expander(
                f"License Scope {index}: "
                f"{item.get('classification', 'UNKNOWN')}"
            ):

                classification = item.get(
                    "classification", "UNKNOWN"
                )

                if classification == "LICENSE_SCOPE_UNCLEAR":
                    st.warning(classification)
                elif classification == "LICENSE_SCOPE_CONFIRMED":
                    st.success(classification)
                else:
                    st.info(classification)

                st.write(
                    "**License:**",
                    item.get("license_name", "N/A")
                )

                st.write(
                    "**Version:**",
                    item.get("license_version", "N/A")
                )

                st.write(
                    "**Scope:**",
                    item.get("scope", "N/A")
                )

                st.write(
                    "**Applicable Section:**",
                    item.get("applicable_section", "N/A")
                )

                pages = item.get("applicable_pages", [])

                if pages:
                    st.write("**Applicable Pages:**", pages)

                supporting = item.get(
                    "supporting_evidence", []
                )

                if supporting:
                    st.write("**Supporting Evidence:**")

                    for evidence in supporting:
                        st.write(f"- {evidence}")

                uncertainties = item.get(
                    "uncertainties", []
                )

                if uncertainties:
                    st.write("**Uncertainties:**")

                    for uncertainty in uncertainties:
                        st.write(f"- {uncertainty}")

    # COPYRIGHT EVIDENCE

    st.markdown("---")
    st.markdown("### 🔎 Evidence Found")

    evidence = report.get("evidence", [])

    if evidence:

        for index, item in enumerate(evidence, 1):

            evidence_type = item.get(
                "type", "Evidence"
            ).replace("_", " ").title()

            page = item.get("page", "N/A")

            with st.expander(
                f"{index}. {evidence_type} — Page {page}"
            ):

                st.write(
                    item.get(
                        "text",
                        "No extracted text available."
                    )
                )

    else:
        st.info("No copyright or license evidence was found.")

    # ORIGINAL SOURCE MATCHES

    st.markdown("---")
    st.markdown("### 🌐 Original Source Matches")

    original_matches = risk.get(
        "original_source_matches", []
    )

    if original_matches:

        for item in original_matches:

            st.markdown(
                f"**{item.get('title', 'Unknown Source')}**"
            )

            st.write(item.get("reason", ""))

            url = clean_url(item.get("url", ""))

            if url:
                st.link_button(
                    "Visit Original Source",
                    url
                )

    else:
        st.info("No original source matches identified.")

    # EXTERNAL SOURCE ANALYSIS

    st.markdown("---")
    st.markdown("### 🔍 External Source Analysis")

    if external_sources:

        for index, item in enumerate(external_sources, 1):

            with st.expander(
                f"{index}. {item.get('title', 'External Source')}"
            ):

                st.write(
                    "**Matched Document Page:**",
                    item.get("document_page", "N/A")
                )

                st.write(
                    "**Similarity Score:**",
                    round(item.get("score", 0), 3)
                )

                st.write(
                    "**Text Overlap:**",
                    f"{item.get('text_overlap', 0)}%"
                )

                st.write(
                    "**Matching Sequences:**",
                    item.get("sequence_match_count", 0)
                )

                st.write("**Matched Query:**")

                st.write(
                    item.get("matched_query", "N/A")
                )

                matched_terms = item.get(
                    "matched_terms", []
                )

                if matched_terms:
                    st.write("**Matched Terms:**")
                    st.write(", ".join(matched_terms))

                url = clean_url(item.get("url", ""))

                if url:
                    st.link_button(
                        "View External Source",
                        url
                    )

    else:
        st.info("No external sources were found.")

    # SOURCE ASSESSMENT

    if source_assessment:

        st.markdown("---")
        st.markdown("### 📊 Source Assessment")

        for index, item in enumerate(source_assessment, 1):

            with st.expander(
                f"{index}. {item.get('title', 'Source Assessment')}"
            ):

                st.write(
                    "**Match Type:**",
                    item.get("match_type", "N/A")
                )

                st.write(
                    "**Document Page:**",
                    item.get("document_page", "N/A")
                )

                st.write(
                    "**Text Overlap:**",
                    f"{item.get('text_overlap', 0)}%"
                )

                st.write(
                    "**Matching Sequences:**",
                    item.get("sequence_match_count", 0)
                )

                st.write(
                    "**Reason:**",
                    item.get("reason", "")
                )

    # RECOMMENDATIONS

    st.markdown("---")
    st.markdown("### 💡 Recommendations")

    if recommendations:

        for index, recommendation in enumerate(
            recommendations, 1
        ):
            st.write(f"{index}. {recommendation}")

    else:
        st.info("No recommendations available.")

    # LIMITATIONS

    if limitations:

        st.markdown("---")
        st.markdown("### ⚠️ Limitations")

        for limitation in limitations:
            st.caption(f"• {limitation}")

    st.caption(
        "This automated assessment provides preliminary findings "
        "and does not constitute formal legal advice."
    )


def show():

    st.markdown("""
    <style>
    .page-heading {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(100deg, #2563eb, #6366f1, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .page-description {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .upload-panel {
        background: linear-gradient(
            135deg,
            rgba(219,234,254,0.85),
            rgba(237,233,254,0.85)
        );
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 22px;
        padding: 25px;
        margin: 15px 0;
    }

    .section-heading {
        color: #312e81;
        font-size: 21px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.85);
        border: 1px dashed #818cf8;
        border-radius: 16px;
        padding: 18px;
    }

    .stButton > button {
        border-radius: 12px;
        min-height: 45px;
        font-weight: 650;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button(
        "← Back to Verifier",
        key="back_pdf_verifier"
    ):
        st.session_state.page = "verifier"
        st.rerun()

    st.markdown("""
    <div class="page-heading">PDF Verification</div>

    <div class="page-description">
        Analyze PDF documents for potential copyright and licensing risks.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-panel">
        <div class="section-heading">📄 Upload Your PDF</div>
        <p style="color:#475569; margin-bottom:0;">
            Select a PDF document to begin the verification process.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1])

    with col1:

        uploaded_file = st.file_uploader(
            "Choose a PDF document",
            type=["pdf"],
            key="verifier_pdf_uploader"
        )

    with col2:

        st.markdown("""
        <div style="
            background:rgba(255,255,255,0.75);
            border:1px solid #c7d2fe;
            border-radius:14px;
            padding:15px;
            margin-top:5px;
        ">
            <div style="color:#4338ca;font-weight:700;">
                Supported Format
            </div>
            <div style="color:#64748b;font-size:14px;margin-top:8px;">
                PDF Documents
            </div>
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file:

        st.markdown("### Selected Document")

        safe_filename = html.escape(uploaded_file.name)

        st.markdown(
            f"""
            <div style="
                background:linear-gradient(110deg,#eff6ff,#f5f3ff);
                border:1px solid #c7d2fe;
                border-radius:15px;
                padding:18px;
            ">
                <div style="color:#312e81;font-weight:700;">
                    📄 {safe_filename}
                </div>
                <div style="color:#64748b;font-size:13px;">
                    PDF document selected for verification
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "🔍 Start PDF Verification",
            type="primary",
            width="stretch",
            key="start_pdf_verification"
        ):

            try:

                with st.spinner(
                    "Analyzing PDF and checking available sources..."
                ):

                    response = requests.post(
                        f"{API_URL}/verifier/verify",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "application/pdf"
                            )
                        },
                        data={
                            "session_id": st.session_state.session_id
                        },
                        timeout=300
                    )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.pdf_verification_result = data

                    st.success(
                        "PDF verification completed!"
                    )

                else:

                    st.error(
                        f"Verification failed: {response.text}"
                    )

            except requests.exceptions.RequestException as e:

                st.error(f"Verification error: {e}")

            except Exception as e:

                st.error(f"Unexpected error: {e}")

    result = st.session_state.get(
        "pdf_verification_result"
    )

    if result:
        show_verification_report(result)
