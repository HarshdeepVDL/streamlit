# app.py
import streamlit as st
import json
from collections import Counter

st.set_page_config(page_title="Document Reviewer — Primary View", layout="wide")

# -------------------------
# Default sample JSON (your provided bicycle-assembly review)
# -------------------------
DEFAULT_JSON = r'''
{
    "document_name": "BICYCLE ASSEMBLY",
    "reviewed_version": "**BICYCLE ASSEMBLY**\n\n**1. REQUIREMENTS**\n**Time:** Not defined.\n**Necessary person(s):** 1.\n**Tools:**\n*   1 Adjustable Wrench (200 mm)\n*   1 set of Hex Keys (2 mm to 10 mm)\n*   1 Phillips Screwdriver (No. 2)\n*   1 Flat Screwdriver (medium)\n*   1 Pedal Wrench (15 mm)\n*   1 Torque Wrench with socket set (5 Nm to 40 Nm range)\n*   (NA) Grease (bicycle grade)\n*   (NA) Clean Cloth\n**Parts:**\n*   1 Bicycle Frame (standard size, steel or aluminium)\n*   1 Front Fork (for 40-inch wheel)\n*   1 Front Wheel (40 inch, with axle and nuts)\n*   1 Rear Wheel (40 inch, with sprocket, axle, and nuts)\n*   2 Tires (40 inch)\n*   2 Inner Tubes (40 inch, with valve)\n*   1 Crankset (right and left crank arms with chainring)\n*   2 Pedals (marked \u201cL\u201d and \u201cR\u201d)\n*   1 Chain (single-speed, compatible with rear sprocket)\n*   1 Chain Guard (plastic or metal, with mounting brackets)\n*   1 Handlebar (straight or curved, standard size)\n*   1 Stem (for handlebar, with clamp bolts)\n*   2 Handlebar Grips\n*   1 Front Brake Caliper (rim brake type, with pads)\n*   1 Rear Brake Caliper (rim brake type, with pads)\n*   2 Brake Levers (left and right, handlebar mount)\n*   2 Brake Cables with housings and end caps\n*   1 Saddle\n*   1 Seat Post\n*   1 Seat Clamp (with bolt or quick-release)\n**Removal of Parts:** No parts to be removed.\n**Summary:**\nTo assemble a standard single-speed bicycle, 40-inch wheels with no gears.\n\n**2. SAFETY INSTRUCTIONS**\n1. Do not assemble the bicycle near moving vehicles or people.\n2. Use correct tools only.\n3. Tighten all screws and nuts to the correct torque.\n4. After assembly, test the bicycle in a safe area.\n\n**3. PREPARE**\n1. Prepare the Frame.\n1.1. Put the bicycle Frame on a Work Stand or a flat surface.\n1.2. Make sure that the Head Tube, Bottom Bracket, and Dropouts are clean.\n1.3. Apply a thin layer of Grease to the Seat Tube (A), Wheel Axles (B) and Pedal Threads (C).\n[Image: Frame on work stand with grease points A, B, C highlighted.]\n\n**4. INSTALL THE FRONT FORK**\n1. Put the Fork Steerer Tube (A) into the Head Tube.\n[Image: Fork Steerer Tube being inserted into the Head Tube.]\n2. Install the Headset Bearings and Spacers.\n[Image: Headset Bearings and Spacers being placed on the Steerer Tube.]\n\n**5. INSTALL THE HANDLEBAR**\n1. Put the Handlebar Stem onto the Steerer Tube.\n[Image: Handlebar Stem being placed on the Steerer Tube.]\nNote: Handlebar Screws will be tightened after the Front Wheel is installed.\n\n**6. INSTALL THE FRONT WHEEL**\n1. Install the Front Wheel Axle into the Fork Dropouts (A).\n[Image: Front Wheel Axle in Fork Dropouts.]\n1.1. Make sure that the Front Wheel is centered.\n1.2. Use the Wrench to tighten the Axle Nuts (A) to 20\u201325 Nm.\n2. Align the Handlebar at 90\u00b0 to the Front Wheel direction.\n[Image: Handlebar aligned with the Front Wheel.]\n3. Use a Hex Key to tighten the Stem Clamp Bolts to 6\u20138 Nm.\n\n**7. INSTALL THE REAR WHEEL**\n1. Put the Chain onto the Rear Sprocket.\n2. Put the Rear Wheel Axle into the Frame Dropouts.\n3. Pull the Rear Wheel back to apply tension to the Chain.\n4. Make sure that the Rear Wheel is centered.\n5. Use the Wrench to tighten the Axle Nuts to 30\u201335 Nm.\n\n**8. INSTALL THE SADDLE**\n1. Put the Saddle Post into the Seat Tube.\n2. Adjust the Saddle Height.\n3. Use a Hex Key to tighten the Seat Clamp Bolt to 10\u201312 Nm.\n\n**9. INSTALL THE PEDALS**\n1. Identify left and right Pedals (marked \u201cL\u201d and \u201cR\u201d).\n2. Apply Grease to the Pedal Threads.\n3. Install the Right Pedal (clockwise).\n3.1. Use the Pedal Wrench to tighten the Right Pedal to 35\u201340 Nm.\n4. Install the Left Pedal (counterclockwise).\n4.1. Use the Pedal Wrench to tighten the Left Pedal to 35\u201340 Nm.\n\n**10. INSTALL THE CHAIN GUARD**\n1. Put the Chain Guard around the Chain and Chainring.\n2. Use two M5 Screws and two Washers to install the Chain Guard to the Frame.\n2.1. Use a Phillips Screwdriver to tighten the M5 Screws to 4\u20135 Nm.\n\n**11. INSTALL THE HAND BRAKES**\n1. Use one M6 Bolt to install the Front Brake Caliper to the Fork.\n1.1. Use a Hex Key to tighten the M6 Bolt to 6\u20137 Nm.\n2. Use one M6 Bolt to install the Rear Brake Caliper to the Frame.\n2.1. Use a Hex Key to tighten the M6 Bolt to 6\u20137 Nm.\n3. Use two Clamp Screws to install the Brake Levers to the Handlebar.\n3.1. Use a Hex Key to tighten the Screws to 5 Nm.\n4. Connect the Brake Cables to the Calipers.\n5. Adjust the Brake Cable Tension so that the Brake Pads contact the Rims equally.\n6. Pull the Brake Levers to test the Brake operation.\n\n**12. FINAL CHECK**\n1. Make sure that the Wheels spin freely.\n2. Make sure that the Chain has 10\u201315 mm vertical movement.\n3. Make sure that the Pedals rotate smoothly.\n4. Make sure that the Saddle and Handlebar are secure.\n5. Test the Brakes.\nNote: Both Wheels must stop the bicycle firmly.\n\n**13. COMPLETE THE ACTIONS**\nNote: No final actions are required.",
    "items": [
        {
            "id": "reqs-tools-capitalization-001",
            "section": "Chapter 1",
            "line_number": 8,
            "sentence": "1 adjustable wrench (200 mm)",
            "status": "red",
            "description": "Named tools in the list are not capitalized as required.",
            "rule_text": "Use initial capital letter for named parts and tools.",
            "normalized_rule": "use initial capital letter for named parts and tools.",
            "reference_pos": "Document body: General rules h",
            "source_file": null,
            "rule_category_id": null,
            "suggestions": [
                {
                    "original_sentence": "1 adjustable wrench (200 mm)",
                    "broken_rule": "The tool name 'adjustable wrench' must start with initial capital letters.",
                    "corrected_example": "1 Adjustable Wrench (200 mm)"
                }
            ],
            "flags": []
        },
        {
            "id": "safety-ste-001",
            "section": "Chapter 2",
            "line_number": 49,
            "sentence": "4. After assembly, then test the bicycle in a safe area.",
            "status": "yellow",
            "description": "The word 'then' is redundant and violates Simplified Technical English (STE) principles.",
            "rule_text": "Write in Simplified Technical English (STE), refer to ASD STE 100 Simplified Technical English.",
            "normalized_rule": "write in simplified technical english (ste), refer to asd ste 100 simplified technical english.",
            "reference_pos": "Document body: General rules a",
            "source_file": null,
            "rule_category_id": null,
            "suggestions": [
                {
                    "original_sentence": "4. After assembly, then test the bicycle in a safe area.",
                    "broken_rule": "STE requires removing unnecessary words. 'Then' is redundant in this context.",
                    "corrected_example": "4. After assembly, test the bicycle in a safe area."
                }
            ],
            "flags": []
        },
        {
            "id": "prepare-image-001",
            "section": "Chapter 3",
            "line_number": 56,
            "sentence": "See image below.",
            "status": "red",
            "description": "The text references an image, but no image is present.",
            "rule_text": "Use images to provide better overview of actions.",
            "normalized_rule": "use images to provide better overview of actions.",
            "reference_pos": "Document body: General rules f",
            "source_file": null,
            "rule_category_id": null,
            "suggestions": [
                {
                    "original_sentence": "See image below.",
                    "broken_rule": "A reference to an image was made, but the image is missing.",
                    "corrected_example": "See image below.\n[Image: Frame on work stand with grease points A, B, C highlighted.]"
                }
            ],
            "flags": [
                "missing image"
            ]
        },
        {
            "id": "chapter-4-title-001",
            "section": "Chapter 4",
            "line_number": 58,
            "sentence": "**4. INSTALL THE FRONT FORK AND HANDLEBAR **",
            "status": "red",
            "description": "Chapter title contains two subjects ('FRONT FORK' and 'HANDLEBAR'), violating the one-subject-per-chapter rule.",
            "rule_text": "One subject per chapter.",
            "normalized_rule": "one subject per chapter.",
            "reference_pos": "Document Header 2",
            "source_file": null,
            "rule_category_id": null,
            "suggestions": [
                {
                    "original_sentence": "**4. INSTALL THE FRONT FORK AND HANDLEBAR **",
                    "broken_rule": "A chapter title must only contain one subject.",
                    "corrected_example": "**4. INSTALL THE FRONT FORK**\n\n... (fork installation steps) ...\n\n**5. INSTALL THE HANDLEBAR**"
                }
            ],
            "flags": []
        },
        {
            "id": "chapter-5-syntax-001",
            "section": "Chapter 5",
            "line_number": 71,
            "sentence": "1.2. Tighten the Axle Nuts (A) with the Wrench to 20\u201325 Nm.",
            "status": "red",
            "description": "The step uses a tool but does not start with the required 'Use the \u2018Tool\u2019 to\u2026' syntax.",
            "rule_text": "If tools are used for an activity, then the step must start with the following syntax: EX.: Use the \u2018Tool\u2019 to\u2026 -> Use the Screwdriver to\u2026",
            "normalized_rule": "if tools are used for an activity, then the step must start with the following syntax: ex.: use the \u2018tool\u2019 to\u2026 -> use the screwdriver to\u2026",
            "reference_pos": "Document body: Steps for Parts and Tools a",
            "source_file": null,
            "rule_category_id": null,
            "suggestions": [
                {
                    "original_sentence": "1.2. Tighten the Axle Nuts (A) with the Wrench to 20\u201325 Nm.",
                    "broken_rule": "A step using a tool must begin with 'Use the [Tool name] to...'.",
                    "corrected_example": "1.2. Use the Wrench to tighten the Axle Nuts (A) to 20\u201325 Nm."
                }
            ],
            "flags": []
        },
        {
            "id": "chapter-5-syntax-002",
            "section": "Chapter 5",
            "line_number": 76,
            "sentence": "3. Tighten the Stem Clamp Bolts with a Hex Key to 6\u20138 Nm.",
            "status": "red",
            "description": "The step uses a tool but does not start with the required 'Use the \u2018Tool\u2019 to\u2026' syntax.",
            "rule_text": "If tools are used for an activity, then the step must start with the following syntax: EX.: Use the \u2018Tool\u2019 to\u2026 -> Use the Screwdriver to\u2026",
            "normalized_rule": "if tools are used for an activity, then the step must start with the following syntax: ex.: use the \u2018tool\u2019 to\u2026 -> use the screwdriver to\u2026",
            "reference_pos": "Document body: Steps for Parts and Tools a",
            "source_file": null,
            "rule_category_id": null,
            "suggestions": [
                {
                    "original_sentence": "3. Tighten the Stem Clamp Bolts with a Hex Key to 6\u20138 Nm.",
                    "broken_rule": "A step using a tool must begin with 'Use the [Tool name] to...'.",
                    "corrected_example": "3. Use a Hex Key to tighten the Stem Clamp Bolts to 6\u20138 Nm."
                }
            ],
            "flags": []
        },
        {
            "id": "chapter-9-syntax-001",
            "section": "Chapter 9",
            "line_number": 100,
            "sentence": "2.1. Use M5 Screws and Washers.",
            "status": "red",
            "description": "The step uses parts but is not a complete action sentence and does not follow the required syntax.",
            "rule_text": "If parts or requirements are used for an activity, then the step must start with the following syntax: EX.: Use [quantity] \u2018Part\u2019 to\u2026 -> Use four Screws to\u2026",
            "normalized_rule": "if parts or requirements are used for an activity, then the step must start with the following syntax: ex.: use [quantity] \u2018part\u2019 to\u2026 -> use four screws to\u2026",
            "reference_pos": "Document body: Steps for Parts and Tools b",
            "source_file": null,
            "rule_category_id": null,
            "suggestions": [
                {
                    "original_sentence": "2.1. Use M5 Screws and Washers.",
                    "broken_rule": "A step using parts must be a complete sentence describing an action, e.g., 'Use [quantity] [Part] to [action]'.",
                    "corrected_example": "2. Use two M5 Screws and two Washers to install the Chain Guard to the Frame."
                }
            ],
            "flags": []
        },
        {
            "id": "chapter-10-capitalization-001",
            "section": "Chapter 10",
            "line_number": 108,
            "sentence": "3. Use Clamp Screws to install the brake Levers to the Handlebar.",
            "status": "yellow",
            "description": "The named part 'brake Levers' is not correctly capitalized.",
            "rule_text": "Use initial capital letter for named parts and tools.",
            "normalized_rule": "use initial capital letter for named parts and tools.",
            "reference_pos": "Document body: General rules h",
            "source_file": null,
            "rule_category_id": null,
            "suggestions": [
                {
                    "original_sentence": "3. Use Clamp Screws to install the brake Levers to the Handlebar.",
                    "broken_rule": "The named part 'brake Levers' should be 'Brake Levers'.",
                    "corrected_example": "3. Use Clamp Screws to install the Brake Levers to the Handlebar."
                }
            ],
            "flags": []
        },
        {
            "id": "chapter-11-ste-001",
            "section": "Chapter 11",
            "line_number": 119,
            "sentence": "5. Do a test of the brakes.",
            "status": "yellow",
            "description": "The phrasing 'Do a test of' is not good STE. A more direct command is preferred. Also, 'brakes' should be capitalized.",
            "rule_text": "Write in Simplified Technical English (STE), refer to ASD STE 100 Simplified Technical English.",
            "normalized_rule": "write in simplified technical english (ste), refer to asd ste 100 simplified technical english.",
            "reference_pos": "Document body: General rules a",
            "source_file": null,
            "rule_category_id": null,
            "suggestions": [
                {
                    "original_sentence": "5. Do a test of the brakes.",
                    "broken_rule": "Use direct, clear commands in STE. The named part 'brakes' should be capitalized.",
                    "corrected_example": "5. Test the Brakes."
                }
            ],
            "flags": []
        },
        {
            "id": "chapter-duplicate-001",
            "section": "Chapter 5 (Duplicate)",
            "line_number": 122,
            "sentence": "**5. COMPLETE THE ACTIONS **",
            "status": "red",
            "description": "The chapter number '5' is a duplicate; the previous chapter was '11'. This breaks the document's sequential structure.",
            "rule_text": "Divide the document in chapters.",
            "normalized_rule": "divide the document in chapters.",
            "reference_pos": "Document body: General rules c",
            "source_file": null,
            "rule_category_id": null,
            "suggestions": [
                {
                    "original_sentence": "**5. COMPLETE THE ACTIONS **",
                    "broken_rule": "Chapters must be numbered sequentially. This should be chapter 12.",
                    "corrected_example": "**12. COMPLETE THE ACTIONS**"
                }
            ],
            "flags": [
                "broken reference"
            ]
        }
    ]
}
'''
# -------------------------
# Utility helpers
# -------------------------
def status_to_color(status: str) -> str:
    s = (status or "").strip().lower()
    if s in ("red", "issue", "error", "fail"):
        return "#e74c3c"  # red
    if s in ("yellow", "warning", "caution"):
        return "#f39c12"  # yellow/orange
    if s in ("green", "good", "ok", "pass"):
        return "#2ecc71"  # green
    return "#7f8c8d"      # gray

def badge_html(status: str) -> str:
    col = status_to_color(status)
    label = (status or "UNKNOWN").upper()
    return f'<span style="background:{col}; color:white; padding:4px 10px; border-radius:8px; font-weight:700;">{label}</span>'

def load_review_json(uploaded_file):
    if uploaded_file is not None:
        try:
            return json.load(uploaded_file)
        except Exception as e:
            st.sidebar.error(f"Could not read uploaded JSON: {e}")
            return None
    # fallback to default
    try:
        return json.loads(DEFAULT_JSON)
    except Exception as e:
        st.sidebar.error(f"Internal sample JSON invalid: {e}")
        return None

# -------------------------
# Sidebar: upload / filters
# -------------------------
st.sidebar.header("Input & Filters")
uploaded = st.sidebar.file_uploader("Upload a review JSON (optional). If none uploaded, built-in sample will be used.", type="json")
data = load_review_json(uploaded)

if not data:
    st.stop()

items = data.get("items", []) or []
statuses = sorted({(it.get("status") or "unknown").title() for it in items})
selected_statuses = st.sidebar.multiselect("Show statuses", options=statuses, default=statuses)
search_q = st.sidebar.text_input("Search (sentence / rule_text / id)", value="").strip()

# -------------------------
# Header + counts
# -------------------------
doc_name = data.get("document_name", "Untitled Document")
st.title(f"📘 {doc_name} — Review Summary")

total = len(items)
counts = Counter([ (it.get("status") or "unknown").lower() for it in items ])
col1, col2, col3 = st.columns([1,1,1])
col1.metric("Total findings", total)
col2.metric("Red / Issue", counts.get("red", 0))
col3.metric("Yellow / Warning", counts.get("yellow", 0))

st.markdown("---")
st.write("Showing **primary information**: Flag, Incorrect sentence, Suggested correction(s), and Broken rule.")

# -------------------------
# Filter items
# -------------------------
def matches_filter(it):
    stt = (it.get("status") or "unknown").title()
    if stt not in selected_statuses:
        return False
    if not search_q:
        return True
    q = search_q.lower()
    hay = " ".join([
        str(it.get("sentence") or ""),
        str(it.get("rule_text") or ""),
        " ".join([s.get("corrected_example","") for s in (it.get("suggestions") or [])]),
        str(it.get("id") or ""),
        str(it.get("section") or "")
    ]).lower()
    return q in hay

filtered = [it for it in items if matches_filter(it)]

if not filtered:
    st.info("No findings match the current filters.")
else:
    # Display each finding as a compact card (expander)
    for it in filtered:
        fid = it.get("id", "")
        sec = it.get("section", "")
        line = it.get("line_number", "")
        status = it.get("status", "Unknown")
        sentence = it.get("sentence", "")
        rule = it.get("rule_text", "") or it.get("normalized_rule", "")
        suggestions = it.get("suggestions") or []
        flags = it.get("flags") or []

        title = f"{fid}  —  {sec}  —  Line {line}"
        with st.expander(title, expanded=False):
            left, right = st.columns([1, 5])
            # Left column: badge + small meta
            left.markdown(badge_html(status), unsafe_allow_html=True)
            left.write(f"**Line**\n{line}")
            left.write(f"**ID**\n{fid}")
            if flags:
                # show small inline tags
                tags_html = " ".join(f'<span style="display:inline-block;background:#ddd;padding:3px 8px;border-radius:6px;margin:2px;font-size:12px;">{f}</span>' for f in flags)
                left.markdown("**Flags**")
                left.markdown(tags_html, unsafe_allow_html=True)

            # Right column: primary info
            
            right.markdown("**📏 Broken rule / Reason**")
            right.write(rule or "-")
            
            right.markdown("**❌ Incorrect sentence**")
            right.code(sentence or "-")

            right.markdown("**✅ Suggested correction(s)**")
            if suggestions:
                for s in suggestions:
                    corr = s.get("corrected_example") or s.get("correction") or ""
                    if corr:
                        # right.markdown(f"- {corr}")
                        right.code(corr or "-")
                    else:
                        right.markdown("- (no correction example provided)")
            else:
                right.markdown("_No suggestions provided._")

# -------------------------
# Footer: show raw reviewed markdown (collapsed)
# -------------------------
st.markdown("---")
with st.expander("📄 Show reviewed document (raw markdown) — optional", expanded=False):
    rv = data.get("reviewed_version", "")
    if rv:
        st.markdown(rv)
    else:
        st.write("No reviewed markdown in JSON.")



