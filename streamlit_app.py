# Task Management Streamlit Application
# Run with: streamlit run streamlit_app.py

import streamlit as st
import os
from dotenv import load_dotenv
from tools import Tools
from agent import generate

load_dotenv()

# Set page config
st.set_page_config(
    page_title="Task Management System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Sidebar Navigation
st.sidebar.title("🎯 Task Manager")
page = st.sidebar.radio("Navigation", ["Login/Register", "Dashboard", "AI Assistant"])

# Page: Login/Register
if page == "Login/Register":
    st.title("🔐 Login / Register")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        login_email = st.text_input("Email (Login)", key="login_email")
        login_password = st.text_input("Password (Login)", type="password", key="login_password")
        
        if st.button("🔓 Login", use_container_width=True):
            if login_email and login_password:
                try:
                    result = Tools.login(login_email, login_password)
                    if "access_token" in result:
                        st.session_state.token = result["access_token"]
                        st.session_state.user_email = login_email
                        st.success(f"✅ Login successful! Welcome {login_email}")
                        st.balloons()
                    else:
                        st.error("❌ Login failed: Invalid credentials")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter email and password")
    
    with col2:
        st.subheader("Register")
        register_email = st.text_input("Email (Register)", key="register_email")
        register_password = st.text_input("Password (Register)", type="password", key="register_password")
        register_confirm = st.text_input("Confirm Password", type="password", key="register_confirm")
        
        if st.button("📝 Register", use_container_width=True):
            if register_email and register_password and register_confirm:
                if register_password != register_confirm:
                    st.error("❌ Passwords don't match")
                else:
                    try:
                        result = Tools.create_user(register_email, register_password)
                        if "id" in result or "access_token" in result:
                            st.success("✅ Registration successful! Please login.")
                        else:
                            st.error(f"❌ Registration failed: {result}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please fill in all fields")
    
    # Logout button
    if st.session_state.token:
        st.divider()
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.token = None
            st.session_state.user_email = None
            st.session_state.tasks = []
            st.success("✅ Logged out successfully!")
            st.rerun()


# Page: Dashboard (requires login)
elif page == "Dashboard":
    if not st.session_state.token:
        st.warning("⚠️ Please login first to access the dashboard")
        st.info("Navigate to 'Login/Register' to authenticate")
    else:
        st.title(f"📊 Dashboard - {st.session_state.user_email}")
        
        # Tabs for different operations
        tab1, tab2, tab3, tab4 = st.tabs(["📋 View Tasks", "➕ Create Task", "✏️ Update Task", "🗑️ Delete Task"])
        
        # Tab 1: View Tasks
        with tab1:
            st.subheader("Your Tasks")
            if st.button("🔄 Refresh Tasks", key="refresh_tasks"):
                try:
                    st.session_state.tasks = Tools.get_tasks(st.session_state.token)
                except Exception as e:
                    st.error(f"Error fetching tasks: {str(e)}")
            
            if st.session_state.tasks:
                for i, task in enumerate(st.session_state.tasks, 1):
                    with st.container():
                        col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
                        
                        with col1:
                            st.metric("ID", task.get("id", "N/A"))
                        
                        with col2:
                            st.write(f"**{task.get('title', 'Untitled')}**")
                            st.caption(task.get('description', 'No description'))
                        
                        with col3:
                            priority = task.get('priority', 'medium').upper()
                            if priority == 'HIGH':
                                st.error(priority)
                            elif priority == 'MEDIUM':
                                st.warning(priority)
                            else:
                                st.success(priority)
                        
                        with col4:
                            status = task.get('completed', False)
                            st.toggle("Done", value=status, key=f"task_status_{i}")
                        
                        st.divider()
            else:
                st.info("📭 No tasks found. Create one to get started!")
        
        # Tab 2: Create Task
        with tab2:
            st.subheader("Create New Task")
            
            with st.form("create_task_form"):
                title = st.text_input("Task Title", placeholder="Enter task title")
                description = st.text_area("Task Description", placeholder="Enter task description", height=100)
                priority = st.selectbox("Priority", ["low", "medium", "high"])
                submit = st.form_submit_button("✅ Create Task", use_container_width=True)
                
                if submit:
                    if title and description:
                        try:
                            result = Tools.create_task(
                                st.session_state.token,
                                title,
                                description,
                                priority
                            )
                            st.success("✅ Task created successfully!")
                            st.json(result)
                            # Refresh tasks
                            st.session_state.tasks = Tools.get_tasks(st.session_state.token)
                        except Exception as e:
                            st.error(f"Error creating task: {str(e)}")
                    else:
                        st.warning("⚠️ Please fill in all required fields")
        
        # Tab 3: Update Task
        with tab3:
            st.subheader("Update Task")
            
            # First, load tasks if not already loaded
            if not st.session_state.tasks:
                try:
                    st.session_state.tasks = Tools.get_tasks(st.session_state.token)
                except Exception as e:
                    st.error(f"Error fetching tasks: {str(e)}")
            
            if st.session_state.tasks:
                task_options = {f"{t['id']}: {t['title']}": t['id'] for t in st.session_state.tasks}
                selected_task = st.selectbox("Select Task to Update", list(task_options.keys()))
                task_id = task_options[selected_task]
                
                # Find the task details
                current_task = next((t for t in st.session_state.tasks if t['id'] == task_id), None)
                
                if current_task:
                    with st.form("update_task_form"):
                        new_title = st.text_input("New Title", value=current_task.get('title', ''))
                        new_description = st.text_area("New Description", value=current_task.get('description', ''), height=100)
                        new_priority = st.selectbox("New Priority", ["low", "medium", "high"], 
                                                   index=["low", "medium", "high"].index(current_task.get('priority', 'medium')))
                        submit = st.form_submit_button("✏️ Update Task", use_container_width=True)
                        
                        if submit:
                            try:
                                result = Tools.update_task(
                                    st.session_state.token,
                                    task_id,
                                    new_title or None,
                                    new_description or None,
                                    new_priority
                                )
                                st.success("✅ Task updated successfully!")
                                st.json(result)
                                # Refresh tasks
                                st.session_state.tasks = Tools.get_tasks(st.session_state.token)
                            except Exception as e:
                                st.error(f"Error updating task: {str(e)}")
            else:
                st.info("📭 No tasks to update")
        
        # Tab 4: Delete Task
        with tab4:
            st.subheader("Delete Task")
            
            # First, load tasks if not already loaded
            if not st.session_state.tasks:
                try:
                    st.session_state.tasks = Tools.get_tasks(st.session_state.token)
                except Exception as e:
                    st.error(f"Error fetching tasks: {str(e)}")
            
            if st.session_state.tasks:
                task_options = {f"{t['id']}: {t['title']}": t['id'] for t in st.session_state.tasks}
                selected_task = st.selectbox("Select Task to Delete", list(task_options.keys()), key="delete_select")
                task_id = task_options[selected_task]
                
                st.warning(f"⚠️ Are you sure you want to delete this task?")
                
                if st.button("🗑️ Delete Task", use_container_width=True, key="delete_btn"):
                    try:
                        result = Tools.delete_task(st.session_state.token, task_id)
                        st.success("✅ Task deleted successfully!")
                        st.json(result)
                        # Refresh tasks
                        st.session_state.tasks = Tools.get_tasks(st.session_state.token)
                    except Exception as e:
                        st.error(f"Error deleting task: {str(e)}")
            else:
                st.info("📭 No tasks to delete")


# Page: AI Assistant
elif page == "AI Assistant":
    if not st.session_state.token:
        st.warning("⚠️ Please login first to use the AI Assistant")
        st.info("Navigate to 'Login/Register' to authenticate")
    else:
        st.title("🤖 AI Task Assistant")
        st.write("Get help from our AI assistant for task management using natural language!")
        
        st.subheader("Chat with AI")
        user_message = st.text_area(
            "What would you like to do?",
            placeholder="Example: Create a task to buy groceries with high priority\nOr: Show me all my tasks\nOr: Delete the task with ID 1",
            height=100
        )
        
        if st.button("💬 Send to AI Assistant", use_container_width=True):
            if user_message:
                with st.spinner("🤔 AI is thinking..."):
                    try:
                        # Create a more detailed prompt with user token
                        enhanced_message = f"{user_message}\n\n[User Token: {st.session_state.token[:20]}...]"
                        
                        # Call the AI agent
                        st.write("---")
                        st.subheader("AI Response:")
                        
                        # Capture and display the AI response
                        import sys
                        from io import StringIO
                        
                        old_stdout = sys.stdout
                        sys.stdout = StringIO()
                        
                        try:
                            generate(enhanced_message)
                            output = sys.stdout.getvalue()
                            sys.stdout = old_stdout
                            
                            if output:
                                st.success(output)
                            else:
                                st.info("AI is processing your request...")
                        except Exception as e:
                            sys.stdout = old_stdout
                            st.error(f"Error: {str(e)}")
                        
                        st.write("---")
                        
                    except Exception as e:
                        st.error(f"Error communicating with AI: {str(e)}")
            else:
                st.warning("⚠️ Please enter a message")
        
        # Example prompts
        st.divider()
        st.subheader("💡 Example Prompts")
        examples = [
            "Login user with email test@example.com and password password123",
            "Create a task to finish project with high priority",
            "Show me all my tasks",
            "Update task ID 1 with new title and medium priority",
            "Delete task ID 1"
        ]
        
        for example in examples:
            if st.button(f"Try: {example}", use_container_width=True):
                st.session_state.ai_prompt = example
                st.rerun()


# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: gray; font-size: small;">
    <p>📱 Task Management System powered by Google Gemini AI</p>
    <p>© 2026 - All rights reserved</p>
    </div>
    """, unsafe_allow_html=True)
