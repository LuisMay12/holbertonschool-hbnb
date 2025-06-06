# HBnB Technical Documentation - Part 1

## Structure
part1/
├── architecture/ # High-level design
├── business_logic/ # Core entities
├── sequence_diagrams/ # API flows
└── scripts/ # Validation tools

text

## Verification Checklist
1. Diagrams:
   - [ ] `class_diagram.mmd` shows all 4 entities with relationships
   - [ ] Sequence diagrams cover all CRUD operations

2. Business Rules:
   - [ ] Price ≥ $10 enforced
   - [ ] Rating 1-5 validated
   - [ ] Amenity uniqueness

3. Validation:
```bash
python3 scripts/validate_entities.py
How to Render Diagrams
Install Mermaid CLI:

bash
npm install -g @mermaid-js/mermaid-cli
Generate PNGs:

bash
mmdc -i sequence_diagrams/user_registration.mmd -o diagrams/user_registration.png
text

---

### Key Validations:
1. **Class Diagram**:
   - All 4 entities with correct attributes
   - Proper UML notation for relationships

2. **Sequence Diagrams**:
   - Show layer transitions (API→Business→DB)
   - Include error paths (e.g., email exists)

3. **Business Rules**:
   - Price minimum
   - Rating constraints
   - Audit fields

4. **Executable Validation**:
   - Script verifies core constraints
   - Can be integrated with tests
