import streamlit as st
from services.feedback_service import FeedbackService
from components.cards import page_header

def render_feedback_page():
    """Render the simple modern feedback submission form"""
    page_header(
        "Feedback & Suggestions",
        "We value your input. Share your thoughts to help us improve."
    )

    feedback_service = FeedbackService()

    if 'feedback_submitted' not in st.session_state:
        st.session_state.feedback_submitted = False

    if st.session_state.feedback_submitted:
        with st.container(border=True):
            st.markdown("""
                <div style="text-align: center; padding: 20px 10px;">
                    <div style="font-size: 3.5rem; margin-bottom: 15px; color: var(--accent);"><i class="fas fa-check-circle"></i></div>
                    <h3 style="color: var(--accent); margin-bottom: 10px; font-weight: 600;">Thank You for Your Feedback!</h3>
                    <p style="color: var(--text-secondary); line-height: 1.6; margin-bottom: 25px;">
                        Your thoughts and suggestions help us improve Smart Resume. 
                        We review every submission carefully!
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Submit Another Response", use_container_width=True):
                st.session_state.feedback_submitted = False
                st.rerun()
    else:
        with st.container(border=True):
            st.markdown("""
                <div style="margin-bottom: 20px;">
                    <h3 style="margin: 0 0 5px 0; font-weight: 600;">Share Your Thoughts</h3>
                    <p style="margin: 0; font-size: 0.9rem; color: var(--text-secondary);">Help us improve by submitting a quick report or suggestion.</p>
                </div>
            """, unsafe_allow_html=True)

            category = st.selectbox(
                "Feedback Category",
                options=["Bug Report", "Feature Request", "Improvement Suggestion", "General Feedback"],
                index=3
            )

            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name (optional)", placeholder="Your Name")
            with col2:
                email = st.text_input("Email (optional)", placeholder="Your Email Address")

            feedback_text = st.text_area(
                "Feedback Detail",
                placeholder="Please write your feedback or suggestions here...",
                height=140
            )

            st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)

            if st.button("Submit Feedback", key="submit_feedback", use_container_width=True, type="primary"):
                if not feedback_text.strip():
                    st.error("Please enter your feedback detail before submitting.")
                else:
                    try:
                        feedback_data = {
                            'rating': 5,
                            'usability_score': 5,
                            'feature_satisfaction': 5,
                            'missing_features': category,
                            'improvement_suggestions': f"Name: {name or 'Anonymous'}\nEmail: {email or 'N/A'}",
                            'user_experience': feedback_text,
                            'name': name,
                            'email': email,
                            'category': category,
                            'feedback_text': feedback_text
                        }
                        feedback_service.save_feedback(feedback_data)
                        
                        st.session_state.feedback_submitted = True
                        st.balloons()
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error submitting feedback: {str(e)}")
