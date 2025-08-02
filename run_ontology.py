import os
import sys
from owlready2 import get_ontology, sync_reasoner_pellet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import cm

def choose_color_class(choice):
    return {
        "1": "BluePostitProduct",
        "2": "GreenPostitProduct",
        "3": "PinkPostitProduct",
        "4": "YellowPostitProduct"
    }.get(choice)

def main():
    # 1) Gather inputs
    client_name = input("Enter your name: ").strip()
    print("""
Select a post-it color:
  1) Blue
  2) Green
  3) Pink
  4) Yellow
""")
    choice   = input("Choice [1-4]: ").strip()
    cls_name = choose_color_class(choice)
    if not cls_name:
        sys.exit(1)
    
    # 2) Load ontology
    script_dir = os.path.dirname(os.path.abspath(__file__))
    owl_file   = os.path.join(script_dir, "postit_product_updated.rdf")
    onto = get_ontology(owl_file).load()

    # 3) Create order individual
    order_id   = f"{client_name.replace(' ', '_')}_Order"
    OrderClass = onto.search_one(iri=f"*#{cls_name}")
    order      = OrderClass(order_id)

    # 4) Save updated ontology
    updated = os.path.join(script_dir, "postit_product_updated.rdf")
    onto.world.save(file=updated, format="rdfxml")

    # 5) Run reasoner
    with onto:
        sync_reasoner_pellet(
            infer_property_values=True,
            infer_data_property_values=True
        )

    # 6) Collect instructions
    sorted_steps = sorted(
        order.hasAssemblyStep,
        key=lambda s: s.sequence[0] if s.sequence else 0
    )
    instructions = [
        step.instruction[0].rstrip()
        for step in sorted_steps
    ]

    # 7) Generate PDF
    pdf_path = os.path.join(script_dir, f"{client_name.replace(' ', '_')}_instructions.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=LETTER,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="PDFTitle", fontSize=16, leading=20))
    styles.add(ParagraphStyle(name="PDFBody",  fontSize=12, leading=16))

    story = [
        Paragraph(f"Instructions for {client_name}'s Order", styles["PDFTitle"]),
        Spacer(1, 12)
    ]

    items = [
        ListItem(Paragraph(instr, styles["PDFBody"]), leftIndent=0)
        for i, instr in enumerate(instructions, start=1)
    ]
    numbered = ListFlowable(items, bulletType="1", start="1", leftIndent=12)
    story.append(numbered)

    doc.build(story)

if __name__ == "__main__":
    main()
