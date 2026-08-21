import json
from abc import ABC, abstractmethod
from pathlib import Path
import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EduPulse | Modern School Operations Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATABASE = "school_data.json"

# Inject Custom High-End Modern CSS & Typography
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global Typography Reset */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Gradient Background Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }
    .metric-badge {
        display: inline-block;
        margin-top: 12px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    /* Custom Header Design */
    .app-header {
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 1.5rem;
    }
    .app-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .app-header p {
        color: #94A3B8;
        font-size: 1rem;
        margin-top: 6px;
    }

    /* Custom Form Containers */
    .form-container {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 32px;
        backdrop-filter: blur(16px);
    }

    /* Styled User Info Cards */
    .user-profile-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-top: 1rem;
    }
    .profile-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .profile-subtitle {
        color: #64748B;
        font-size: 0.9rem;
    }

    /* Hide Default Elements for Cleanliness */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA PERSISTENCE & ENGINE
# -----------------------------------------------------------------------------
def load_data():
    if Path(DATABASE).exists():
        try:
            with open(DATABASE, "r") as f:
                content = f.read()
                if content:
                    return json.loads(content)
        except Exception as err:
            st.error(f"Error loading database: {err}")
    return {"student": [], "teachers": []}

def save_data(data):
    try:
        with open(DATABASE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as err:
        st.error(f"Error saving database: {err}")

if "data" not in st.session_state:
    st.session_state["data"] = load_data()

# -----------------------------------------------------------------------------
# 3. DOMAIN OOP CLASSES
# -----------------------------------------------------------------------------
class Persons(ABC):
    @abstractmethod
    def get_roles(self):
        pass

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email

class Students(Persons):
    def get_roles(self):
        return "Student"

    def register(self, name, age, roll_no, email):
        if not self.validate_email(email):
            return False, "Please enter a valid email address."
        
        data = st.session_state["data"]
        for s in data["student"]:
            if s["roll_no"] == roll_no:
                return False, f"Roll Number #{roll_no} is already assigned to another student."

        data["student"].append({
            "name": name,
            "age": age,
            "roll_no": roll_no,
            "email": email,
            "grades": {}
        })
        save_data(data)
        return True, f"Student **{name}** registered successfully."

    def add_grade(self, roll_no, subject, marks):
        data = st.session_state["data"]
        for s in data["student"]:
            if s["roll_no"] == roll_no:
                s["grades"][subject] = marks
                save_data(data)
                return True, f"Updated **{subject}** score to **{marks}** for {s['name']}."
        return False, "Student record not found."

class Teacher(Persons):
    def get_roles(self):
        return "Teacher"

    def register(self, name, age, emp_id, subject, email):
        if not self.validate_email(email):
            return False, "Please enter a valid email address."

        data = st.session_state["data"]
        for t in data["teachers"]:
            if t["employee_id"] == emp_id:
                return False, f"Employee ID #{emp_id} is already registered."

        data["teachers"].append({
            "name": name,
            "age": age,
            "employee_id": emp_id,
            "subject": subject,
            "email": email
        })
        save_data(data)
        return True, f"Faculty Member **{name}** onboarded successfully."

student_handler = Students()
teacher_handler = Teacher()

# -----------------------------------------------------------------------------
# 4. NAVIGATION / SIDEBAR DESIGN
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
    <div style="padding: 10px 0px 20px 0px;">
        <h2 style="font-weight: 800; font-size: 1.5rem; letter-spacing: -0.03em; margin: 0; color: #F8FAFC;">
            ⚡ EduPulse <span style="font-size: 0.8rem; font-weight: 600; color: #6366F1; vertical-align: super;">PRO</span>
        </h2>
        <p style="font-size: 0.8rem; color: #64748B; margin: 4px 0 0 0;">Operations Platform</p>
    </div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "NAVIGATION",
    ["Overview Dashboard", "Register Student", "Onboard Faculty", "Academic Grading", "Directory Search"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="background: rgba(99, 102, 241, 0.08); border-radius: 12px; padding: 16px; border: 1px solid rgba(99, 102, 241, 0.2);">
        <p style="font-size: 0.8rem; font-weight: 700; color: #818CF8; margin: 0 0 4px 0;">SYSTEM STATUS</p>
        <p style="font-size: 0.75rem; color: #94A3B8; margin: 0;">🟢 Database Connected<br>JSON Local Storage Dynamic Sync</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. VIEW ROUTER
# -----------------------------------------------------------------------------

# VIEW 1: OVERVIEW DASHBOARD
if menu == "Overview Dashboard":
    st.markdown("""
        <div class="app-header">
            <h1>Executive Overview</h1>
            <p>Real-time analytics and institutional metrics across faculties.</p>
        </div>
    """, unsafe_allow_html=True)

    students = st.session_state["data"]["student"]
    teachers = st.session_state["data"]["teachers"]

    # Calculate metrics
    total_students = len(students)
    total_teachers = len(teachers)
    
    all_scores = []
    for s in students:
        for m in s.get("grades", {}).values():
            all_scores.append(m)
    avg_performance = (sum(all_scores) / len(all_scores)) if all_scores else 0.0

    # Top KPI Cards using Custom HTML Layout
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Active Enrolment</div>
                <div class="metric-value">{total_students}</div>
                <div class="metric-badge">Students Enrolled</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Faculty Members</div>
                <div class="metric-value">{total_teachers}</div>
                <div class="metric-badge" style="background: rgba(168, 85, 247, 0.15); color: #C084FC; border-color: rgba(168, 85, 247, 0.3);">Academic Staff</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Institutional Average</div>
                <div class="metric-value">{avg_performance:.1f}%</div>
                <div class="metric-badge" style="background: rgba(34, 197, 94, 0.15); color: #4ADE80; border-color: rgba(34, 197, 94, 0.3);">Across All Courses</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tables with Streamlit Native Styler
    tab1, tab2 = st.tabs(["🎓 Student Registry", "👩‍🏫 Faculty Directory"])

    with tab1:
        if students:
            # Re-format dict for clean display
            display_students = []
            for s in students:
                grades_count = len(s.get("grades", {}))
                scores = list(s.get("grades", {}).values())
                avg = (sum(scores) / len(scores)) if scores else 0
                display_students.append({
                    "Roll No": f"#{s['roll_no']}",
                    "Name": s['name'],
                    "Age": s['age'],
                    "Email": s['email'],
                    "Subjects Graded": grades_count,
                    "GPA / Avg (%)": f"{avg:.1f}%"
                })
            st.dataframe(display_students, use_container_width=True)
        else:
            st.info("No student records available.")

    with tab2:
        if teachers:
            display_teachers = [{
                "Emp ID": f"#{t['employee_id']}",
                "Faculty Name": t['name'],
                "Subject Area": t['subject'],
                "Age": t['age'],
                "Contact Email": t['email']
            } for t in teachers]
            st.dataframe(display_teachers, use_container_width=True)
        else:
            st.info("No faculty records available.")

# VIEW 2: REGISTER STUDENT
elif menu == "Register Student":
    st.markdown("""
        <div class="app-header">
            <h1>Register Student</h1>
            <p>Onboard a new student into the centralized system.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, _ = st.columns([2, 1])
    with col1:
        with st.form("register_student_form", clear_on_submit=True):
            st.markdown("### Personal & Academic Information")
            name = st.text_input("Full Name", placeholder="e.g. Alexander Pierce")
            email = st.text_input("Email Address", placeholder="e.g. alexander@school.edu")
            
            c1, c2 = st.columns(2)
            age = c1.number_input("Age", min_value=5, max_value=100, value=16)
            roll_no = c2.number_input("Assign Roll Number", min_value=1, step=1, value=101)

            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Submit Registration", use_container_width=True)

            if submit:
                if not name or not email:
                    st.warning("Please complete all required fields.")
                else:
                    success, msg = student_handler.register(name, age, roll_no, email)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

# VIEW 3: ONBOARD FACULTY
elif menu == "Onboard Faculty":
    st.markdown("""
        <div class="app-header">
            <h1>Onboard Faculty</h1>
            <p>Add new academic instructors and staff members.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, _ = st.columns([2, 1])
    with col1:
        with st.form("register_teacher_form", clear_on_submit=True):
            st.markdown("### Faculty Profile Details")
            name = st.text_input("Full Name", placeholder="e.g. Dr. Sarah Vance")
            email = st.text_input("Email Address", placeholder="e.g. s.vance@school.edu")
            subject = st.text_input("Department / Subject Area", placeholder="e.g. Advanced Mathematics")
            
            c1, c2 = st.columns(2)
            age = c1.number_input("Age", min_value=21, max_value=90, value=35)
            emp_id = c2.number_input("Employee ID Number", min_value=1, step=1, value=501)

            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Complete Onboarding", use_container_width=True)

            if submit:
                if not name or not email or not subject:
                    st.warning("Please complete all required fields.")
                else:
                    success, msg = teacher_handler.register(name, age, emp_id, subject, email)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

# VIEW 4: ACADEMIC GRADING
elif menu == "Academic Grading":
    st.markdown("""
        <div class="app-header">
            <h1>Academic Grading Portal</h1>
            <p>Log grades and assign evaluation scores to registered students.</p>
        </div>
    """, unsafe_allow_html=True)

    students = st.session_state["data"]["student"]
    if not students:
        st.warning("No student records found in database. Register a student first.")
    else:
        col1, _ = st.columns([2, 1])
        with col1:
            student_options = {f"{s['name']} (Roll #{s['roll_no']})": s["roll_no"] for s in students}
            selected_label = st.selectbox("Select Target Student", list(student_options.keys()))
            target_roll = student_options[selected_label]

            with st.form("add_grade_form", clear_on_submit=True):
                subject = st.text_input("Subject Course Name", placeholder="e.g. Physics Theory")
                marks = st.slider("Score / Percentage Assessment", min_value=0.0, max_value=100.0, value=85.0, step=0.5)

                st.markdown("<br>", unsafe_allow_html=True)
                submit = st.form_submit_button("Save Course Assessment", use_container_width=True)

                if submit:
                    if not subject:
                        st.warning("Please specify a course subject.")
                    else:
                        success, msg = student_handler.add_grade(target_roll, subject, marks)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)

# VIEW 5: DIRECTORY SEARCH
elif menu == "Directory Search":
    st.markdown("""
        <div class="app-header">
            <h1>Directory Profile Inspector</h1>
            <p>Inspect comprehensive data records for students and faculty members.</p>
        </div>
    """, unsafe_allow_html=True)

    search_type = st.segmented_control("Select Profile Type", ["Student Profiles", "Faculty Profiles"], default="Student Profiles")

    if search_type == "Student Profiles":
        students = st.session_state["data"]["student"]
        if not students:
            st.info("No student records available.")
        else:
            student_map = {f"{s['name']} (Roll #{s['roll_no']})": s for s in students}
            selected_student_name = st.selectbox("Search Student Profile", list(student_map.keys()))
            selected_s = student_map[selected_student_name]

            # Custom Profile Card Display
            st.markdown(f"""
                <div class="user-profile-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="profile-title">{selected_s['name']}</div>
                            <div class="profile-subtitle">Roll Number #{selected_s['roll_no']} • Enrolled Student</div>
                        </div>
                        <div style="background: rgba(99, 102, 241, 0.2); padding: 8px 16px; border-radius: 20px; color: #818CF8; font-weight: 700;">
                            Age: {selected_s['age']}
                        </div>
                    </div>
                    <hr style="border-color: rgba(255,255,255,0.08); margin: 16px 0;">
                    <div style="color: #94A3B8; font-size: 0.9rem;"><strong>Email:</strong> {selected_s['email']}</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📊 Academic Record & Performance")
            grades = selected_s.get("grades", {})

            if grades:
                g_col1, g_col2 = st.columns([2, 1])
                with g_col1:
                    st.dataframe([{"Course": sub, "Score": f"{score}%"} for sub, score in grades.items()], use_container_width=True)
                with g_col2:
                    avg_val = sum(grades.values()) / len(grades)
                    st.markdown(f"""
                        <div class="metric-card" style="text-align: center;">
                            <div class="metric-title">Cumulative Average</div>
                            <div class="metric-value" style="font-size: 2.8rem;">{avg_val:.1f}%</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No academic assessment grades recorded yet for this student.")

    else:
        teachers = st.session_state["data"]["teachers"]
        if not teachers:
            st.info("No faculty records available.")
        else:
            teacher_map = {f"{t['name']} ({t['subject']})": t for t in teachers}
            selected_teacher_name = st.selectbox("Search Faculty Profile", list(teacher_map.keys()))
            selected_t = teacher_map[selected_teacher_name]

            st.markdown(f"""
                <div class="user-profile-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="profile-title">{selected_t['name']}</div>
                            <div class="profile-subtitle">Employee ID #{selected_t['employee_id']} • Academic Staff</div>
                        </div>
                        <div style="background: rgba(168, 85, 247, 0.2); padding: 8px 16px; border-radius: 20px; color: #C084FC; font-weight: 700;">
                            {selected_t['subject']}
                        </div>
                    </div>
                    <hr style="border-color: rgba(255,255,255,0.08); margin: 16px 0;">
                    <div style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 6px;"><strong>Email:</strong> {selected_t['email']}</div>
                    <div style="color: #94A3B8; font-size: 0.9rem;"><strong>Age:</strong> {selected_t['age']} years old</div>
                </div>
            """, unsafe_allow_html=True)