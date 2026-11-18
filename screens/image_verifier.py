
import html

import streamlit as st
import requests

API_URL = "https://sourcechat-ajmal.onrender.com"


def show_list(items, empty_message="No information found."):
    if not items:
        st.caption(empty_message)
        return

    for item in items:
        if isinstance(item, dict):
            title = item.get("title")

            if title:
                st.markdown(f"**{title}**")

            content = (
                item.get("content")
                or item.get("snippet")
                or item.get("description")
                or item.get("detail")
                or item.get("reason")
            )

            if content:
                safe_content = html.escape(str(content))
                st.markdown(
                    f"""
                    <p style="
                        font-size: 14px;
                        line-height: 1.6;
                        font-weight: 400;
                        margin: 4px 0 8px 0;
                    ">{safe_content}</p>
                    """,
                    unsafe_allow_html=True
                )

            url = item.get("url") or item.get("link")

            if url:
                st.markdown(f"[Open Source]({url})")

        else:
            st.markdown(f"- {item}")


def show():
    st.markdown("""
    <style>
    .page-heading {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(100deg, #0f766e, #0891b2, #6366f1);
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
        background: linear-gradient(135deg, rgba(204,251,241,0.75), rgba(224,231,255,0.8));
        border: 1px solid rgba(13,148,136,0.2);
        border-radius: 22px;
        padding: 25px;
        margin: 15px 0;
    }

    .section-heading {
        color: #134e4a;
        font-size: 21px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .result-heading {
        color: #312e81;
        font-size: 25px;
        font-weight: 750;
        margin-bottom: 12px;
    }

    .report-card {
        background: rgba(255,255,255,0.8);
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        padding: 18px;
        margin-bottom: 12px;
    }

    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.85);
        border: 1px dashed #0d9488;
        border-radius: 16px;
        padding: 18px;
    }

    .stButton > button {
        border-radius: 12px;
        min-height: 45px;
        font-weight: 650;
    }

    .source-description {
        font-size: 14px;
        line-height: 1.6;
        font-weight: 400;
        margin: 4px 0 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("← Back to Verifier", key="back_image_verifier"):
        st.session_state.page = "verifier"
        st.rerun()

    st.markdown("""
    <div class="page-heading">Image Verification</div>
    <div class="page-description">
        Analyze images for potential copyright and licensing risks.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-panel">
        <div class="section-heading">🖼️ Upload Your Image</div>
        <p style="color:#475569; margin-bottom:0;">
            Select an image to begin the copyright verification process.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["png", "jpg", "jpeg", "webp"],
            key="verifier_image_uploader"
        )

    with col2:
        st.markdown("""
        <div style="
            background:rgba(255,255,255,0.75);
            border:1px solid #ccfbf1;
            border-radius:14px;
            padding:15px;
            margin-top:5px;
        ">
            <div style="color:#0f766e;font-weight:700;">
                Supported Formats
            </div>
            <div style="color:#64748b;font-size:14px;margin-top:8px;">
                PNG · JPG · JPEG · WEBP
            </div>
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file:
        st.markdown("### Image Preview")

        preview_col, details_col = st.columns([1, 1])

        with preview_col:
            st.image(
                uploaded_file,
                caption=uploaded_file.name,
                use_container_width=True
            )

        with details_col:
            st.markdown("#### Image Details")
            st.write(f"**Filename:** {uploaded_file.name}")
            st.write(f"**File size:** {uploaded_file.size / 1024:.2f} KB")
            st.write(f"**Format:** {uploaded_file.type}")

        if st.session_state.get("image_result_filename") != uploaded_file.name:
            st.session_state.pop("image_verification_result", None)
            st.session_state.pop("image_result_filename", None)

        if st.button(
            "🔍 Start Image Verification",
            type="primary",
            use_container_width=True,
            key="start_image_verification"
        ):
            try:
                with st.spinner("Analyzing image and checking available sources..."):
                    response = requests.post(
                        f"{API_URL}/image-verifier/verify",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                uploaded_file.type
                            )
                        },
                        data={
                            "session_id": st.session_state.session_id
                        },
                        timeout=300
                    )

                if response.status_code == 200:
                    data = response.json()

                    st.session_state.image_verification_result = data
                    st.session_state.image_result_filename = uploaded_file.name

                    st.success("Image verification completed successfully!")

                else:
                    st.error(f"Verification failed: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Verification error: {e}")

    data = st.session_state.get("image_verification_result")

    if not data:
        return

    report = data.get("verification_report", {})

    image_analysis = report.get("image_analysis", {})
    image_metadata = report.get("image_metadata", {})
    image_properties = image_metadata.get("image_properties", {})
    wikimedia = report.get("wikimedia_lookup", {})
    risk = report.get("risk_assessment", {})
    verification_status = risk.get("verification_status", {})

    st.divider()

    st.markdown("""
    <div class="result-heading">
        🛡️ Image Verification Report
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        f"Filename: {data.get('filename', 'Unknown')} "
        f"| Document ID: {data.get('document_id', 'N/A')}"
    )

    risk_level = risk.get("risk_level", "UNKNOWN").upper()

    st.markdown("### Copyright Risk Overview")

    if risk_level == "HIGH":
        st.error(f"🔴 Copyright Risk: {risk_level}")
    elif risk_level == "LOW":
        st.success(f"🟢 Copyright Risk: {risk_level}")
    elif risk_level == "MEDIUM":
        st.warning(f"🟠 Copyright Risk: {risk_level}")
    else:
        st.info(f"🔵 Copyright Risk: {risk_level}")

    st.write(risk.get("summary", "No risk summary available."))

    status_col1, status_col2 = st.columns(2)

    with status_col1:
        st.markdown("**Original Source**")
        source_status = verification_status.get(
            "original_source", "NOT_VERIFIED"
        )
        st.write(source_status.replace("_", " ").title())

    with status_col2:
        st.markdown("**License Status**")
        license_status = verification_status.get(
            "license", "NOT_VERIFIED"
        )
        st.write(license_status.replace("_", " ").title())

    st.divider()

    st.markdown("### 🖼️ Image Analysis")

    st.markdown("**Image Description**")
    st.write(
        image_analysis.get(
            "image_description",
            "No image description available."
        )
    )

    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:
        st.markdown("**Distinctive Visual Features**")
        show_list(
            image_analysis.get("distinctive_visual_features", [])
        )

    with feature_col2:
        st.markdown("**Visible Text**")
        show_list(
            image_analysis.get("visible_text", []),
            "No visible text detected."
        )

    st.markdown("**Copyright Indicators**")
    show_list(
        image_analysis.get("copyright_indicators", []),
        "No visible copyright indicators detected."
    )

    st.markdown("**Possible Creators or Owners**")
    show_list(
        image_analysis.get("possible_creators_or_owners", []),
        "No possible creator or owner identified."
    )

    st.markdown("**Brands or Organizations**")
    show_list(
        image_analysis.get("brands_or_organizations", []),
        "No brands or organizations detected."
    )

    st.divider()

    st.markdown("### 📋 Image Metadata")

    metadata_col1, metadata_col2, metadata_col3 = st.columns(3)

    with metadata_col1:
        st.metric(
            "Format",
            image_properties.get("format", "Unknown")
        )

    with metadata_col2:
        st.metric(
            "Dimensions",
            f"{image_properties.get('width', 'N/A')} × "
            f"{image_properties.get('height', 'N/A')}"
        )

    with metadata_col3:
        st.metric(
            "Metadata Found",
            "Yes" if image_metadata.get("embedded_metadata_found") else "No"
        )

    with st.expander("View Detailed Metadata"):
        st.markdown("**EXIF Information**")
        exif = image_metadata.get("exif", {})

        if exif:
            st.json(exif)
        else:
            st.caption("No EXIF information found.")

        st.markdown("**XMP Information**")
        xmp = image_metadata.get("xmp", {})

        if xmp:
            st.json(xmp)
        else:
            st.caption("No XMP information found.")

        st.markdown("**Metadata Sources**")
        show_list(image_metadata.get("metadata_sources", []))

        st.markdown("**Metadata Limitations**")
        show_list(image_metadata.get("limitations", []))

    st.divider()

    st.markdown("### 🌐 Source Search Results")

    wiki_col1, wiki_col2 = st.columns(2)

    with wiki_col1:
        st.markdown("**Wikimedia Commons Image Match**")

        if wikimedia.get("found"):
            st.success("Potential match found")
        else:
            st.warning("No matching file found")

        st.caption(
            f"Match method: {wikimedia.get('match_method', 'N/A')}"
        )

    with wiki_col2:
        st.markdown("**External Web Search Results**")

        external_sources = report.get("external_sources", [])
        total_sources = report.get("total_sources", len(external_sources))

        st.metric("Sources Found", total_sources)

    with st.expander("View Wikimedia Matches"):
        show_list(
            wikimedia.get("matches", []),
            "No Wikimedia matches found."
        )

        st.markdown("**Search Limitations**")
        show_list(wikimedia.get("limitations", []))

    with st.expander("View External Sources"):
        if external_sources:
            for index, source in enumerate(external_sources, start=1):
                if isinstance(source, dict):
                    title = source.get("title", "External Source")
                    url = source.get("url") or source.get("link")

                    content = (
                        source.get("content")
                        or source.get("snippet")
                        or source.get("description")
                    )

                    st.markdown(f"**{index}. {title}**")

                    if content:
                        safe_content = html.escape(str(content))

                        st.markdown(
                            f"""
                            <p class="source-description">
                                {safe_content}
                            </p>
                            """,
                            unsafe_allow_html=True
                        )

                    if url:
                        st.markdown(f"[View Original Source]({url})")

                    st.divider()

                else:
                    st.write(source)
        else:
            st.info("No usable external sources were obtained.")

    st.caption(
        "External webpages provide contextual information. "
        "They do not independently verify that the uploaded image "
        "is the same image or establish reuse rights."
    )

    st.markdown("**Search Queries Used**")
    show_list(
        report.get("search_queries", []),
        "No search queries available."
    )

    st.divider()

    st.markdown("### ⚖️ Copyright & License Findings")

    findings_col1, findings_col2 = st.columns(2)

    with findings_col1:
        st.markdown("**Ownership Findings**")
        show_list(
            risk.get("ownership_findings", []),
            "No ownership information found."
        )

    with findings_col2:
        st.markdown("**License Findings**")
        show_list(
            risk.get("license_findings", []),
            "No license information found."
        )

    st.markdown("**Possible Source Matches**")
    show_list(
        risk.get("possible_source_matches", []),
        "No possible source matches identified."
    )

    st.divider()

    st.markdown("### 💡 Recommendations")

    recommendations = risk.get("recommendations", [])

    if recommendations:
        for index, recommendation in enumerate(recommendations, start=1):
            st.markdown(f"**{index}.** {recommendation}")
    else:
        st.caption("No recommendations available.")

    with st.expander("⚠️ Important Limitations"):
        show_list(
            risk.get("limitations", []),
            "No limitations reported."
        )

    st.divider()

    st.caption(
        "This is an AI-assisted preliminary copyright and licensing-risk "
        "assessment. It is not legal advice and does not establish "
        "copyright ownership or permission to reuse an image."
    )
