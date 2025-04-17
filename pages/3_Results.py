import os
import streamlit as st
from openai import OpenAI
import random
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# Set page config with light theme
st.set_page_config(page_title="Personality Results", layout="wide", initial_sidebar_state="collapsed")

# Instagram-inspired light theme styling
light_theme_css = """
<style>
    /* Main background and text colors */
    .stApp {
        background-color: #fafafa;
        color: #262626;
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #262626 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Card-like containers */
    .card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid #efefef;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Section titles */
    .section-title {
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 18px;
        color: #262626;
        display: flex;
        align-items: center;
    }
    
    .section-title-icon {
        margin-right: 12px;
        font-size: 32px;
    }
    
    /* Personality title styling */
    .personality-title {
        font-size: 52px;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #fd1d1d, #833ab4, #405de6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
    }
    
    .personality-desc {
        text-align: center;
        font-style: italic;
        font-size: 20px;
        color: #666666;
        margin-bottom: 34px;
    }
    
    /* Trait container styling */
    .trait-container {
        margin-bottom: 20px;
    }
    
    /* Roast button styling */
    .roast-button-container {
        display: flex;
        justify-content: center;
        margin: 30px 0;
    }
    
    .roast-button {
        background: linear-gradient(90deg, #fd1d1d, #833ab4);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 12px 30px;
        font-size: 20px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .roast-button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Roast content */
    .roast-content {
        font-style: italic;
        background: #fff9eb;
        border-radius: 16px;
        padding: 24px;
        margin-top: 16px;
        border-left: 5px solid #e1306c;
        color: #333;
        font-size: 18px;
        line-height: 1.6;
    }
    
    /* Recommendation styling */
    .recommendation-container {
        display: flex;
        flex-direction: column;
        gap: 16px;
    }
    
    .recommendation-item {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        border-left: 4px solid #405de6;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
    }
    
    .recommendation-title {
        font-weight: 700;
        font-size: 18px;
        color: #262626;
        margin-bottom: 8px;
    }
    
    .recommendation-desc {
        color: #666666;
        font-size: 16px;
        line-height: 1.5;
    }
    
    /* Insights styling */
    .insights-container {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .insights-column {
        flex: 1;
        background-color: #ffffff;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
    }
    
    .insights-heading {
        font-weight: 700;
        font-size: 18px;
        margin-bottom: 12px;
        color: #405de6;
    }
    
    .insights-list {
        list-style-type: none;
        padding-left: 0;
    }
    
    .insights-list li {
        padding: 6px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .insights-list li:last-child {
        border-bottom: none;
    }
    
    /* Instagram gradient for special elements */
    .instagram-gradient {
        background: linear-gradient(90deg, #fd1d1d, #833ab4, #405de6);
        padding: 3px;
        border-radius: 16px;
        margin-bottom: 30px;
    }
    
    .instagram-gradient-inner {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 22px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #888888;
        font-size: 14px;
    }
    
    /* Container width adjustment */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Chart styling */
    .chart-container {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 30px;
    }
    
    /* Action buttons */
    .action-button {
        background: linear-gradient(90deg, #405de6, #833ab4);
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .action-button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Make title bold */
    .personality-title strong {
        font-weight: 800;
    }
    
    /* Progress bar styling */
    .chart-container {
        padding-top: 15px;
        padding-bottom: 15px;
    }
</style>
"""

st.markdown(light_theme_css, unsafe_allow_html=True)

# Initialize OpenAI client
try:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")
    client = None
    if st.button("Try Again"):
        st.rerun()
    st.stop()

# Check if there are any responses
if 'convo_log' not in st.session_state or len(st.session_state.convo_log) == 0:
    st.warning("No responses found. Please complete the interview first.")
    if st.button("Return to Start"):
        st.switch_page("pages/1_Welcome.py")
    st.stop()

# Compile responses for analysis
combined = ""
for c in st.session_state.convo_log:
    if 'answer' in c and c['answer']:
        combined += f"Q: {c['question']}\nA: {c['answer']}\n\n"

if not combined:
    st.warning("No valid responses found for analysis.")
    st.stop()

# Function to create a vertical bar chart for personality traits with thinner bars and curved edges
def create_vertical_bar_chart(traits):
    categories = list(traits.keys())
    values = list(traits.values())
    
    # Create a color gradient for bars
    colors = [f'rgba({int(64 + (191-64) * i/len(categories))}, {int(93 + (132-93) * i/len(categories))}, {int(230 + (225-230) * i/len(categories))}, 0.7)' 
              for i in range(len(categories))]
    
    # Create figure
    fig = go.Figure()
    
    # Add bars with thinner width and curved edges
    for i, (cat, val, color) in enumerate(zip(categories, values, colors)):
        fig.add_trace(go.Bar(
            x=[val],
            y=[cat],
            orientation='h',
            marker=dict(
                color=color,
                line=dict(width=0),
                # Add corner radius for curved edges
                cornerradius=10
            ),
            width=0.4,  # Make bars even thinner (lower value = thinner bars)
            text=[f"{val}%"],
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(
                color='white',
                size=14,
                family="Helvetica Neue, Arial"
            ),
            hoverinfo='text',
            hovertext=f"{cat}: {val}%"
        ))
    
    # Update layout
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=10, b=10),
        xaxis=dict(
            range=[0, 105],
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.3)',
            gridwidth=1,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            automargin=True,
            tickfont=dict(
                family="Helvetica Neue, Arial",
                size=14,
                color="#262626"
            )
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        bargap=0.5  # Increase gap between bars
    )
    
    return fig

# Generate base personality analysis if not already done
if 'personality_data' not in st.session_state:
    with st.spinner("Analyzing your personality..."):
        try:
            # Main personality profile
            profile_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are a professional psychologist who specializes in personality assessment.
                    Create a comprehensive personality analysis including:
                    1. A single-word or short phrase personality type title (just the title, no numbering or labels)
                    2. A one-sentence description of this personality type (just the description, no numbering or labels)
                    3. A detailed 2-paragraph personality profile (just the profile, no numbering or labels)
                    4. Percentages for the Big Five traits (Extraversion, Openness, Conscientiousness, Agreeableness, Neuroticism)
                    5. Three adjectives for each trait
                    6. Book recommendations (3 books) with brief descriptions
                    7. Movie recommendations (3 movies) with brief descriptions
                    8. Music recommendations (3 songs/artists) with brief descriptions
                    9. Celebrity doppelgangers - 3 celebrity personality matches with one-sentence descriptions explaining the match
                    10. Relationship insights with 3 strengths and 3 weaknesses
                    11. Career insights with 3 strengths and 3 ideal career paths
                    
                    DO NOT include section numbers or titles like "Personality Type Title:" or "Description:" in your response. 
                    Just provide the content directly."""},
                    {"role": "user", "content": f"Based on the following conversation, analyze this person's personality:\n\n{combined}"}
                ]
            )
            
            # Roast personality analysis
            roast_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are a witty comedian giving a good-natured roast of someone's personality.
                    Be playful and humorous but not mean-spirited. Keep it to 2-3 paragraphs."""},
                    {"role": "user", "content": f"Based on the following conversation, create a friendly roast of this person's personality traits:\n\n{combined}"}
                ]
            )
            
            # Parse the main profile response
            full_analysis = profile_response.choices[0].message.content.strip()
            
            # Store the roast separately
            personality_roast = roast_response.choices[0].message.content.strip()
            
            # Try to extract structured data - this is a simplified approach
            lines = full_analysis.split('\n')
            
            # Extract title and short description (first two lines)
            personality_title = lines[0].strip().replace('#', '').strip() if lines else "The Analyzer"
            personality_desc = lines[1].strip() if len(lines) > 1 else "A balanced personality with unique insights and perspectives."
            
            # Extract main profile (everything until we hit a section heading)
            profile_text = ""
            i = 2
            while i < len(lines) and not any(x in lines[i].lower() for x in ["trait", "big five", "book", "movie", "music", "relationship", "career"]):
                profile_text += lines[i] + " "
                i += 1
            
            # Generate random trait percentages if we can't parse them
            # In a real app, you'd want to extract these from the AI response
            personality_traits = {
                "Extraverted": random.randint(20, 95),
                "Open": random.randint(20, 95),
                "Conscientious": random.randint(20, 95),
                "Agreeable": random.randint(20, 95),
                "Neurotic": random.randint(20, 95)
            }
            
            trait_adjectives = {
                "Extraverted": ["Energetic", "Outgoing", "Social"],
                "Open": ["Curious", "Creative", "Adaptable"],
                "Conscientious": ["Organized", "Reliable", "Disciplined"],
                "Agreeable": ["Compassionate", "Cooperative", "Empathetic"],
                "Neurotic": ["Sensitive", "Emotional", "Self-aware"]
            }
            
            # Extract remaining sections using simple text parsing
            # For a production app, you'd want more robust parsing or ask the model to return structured data
            
            sections = full_analysis.lower().split("book")
            if len(sections) > 1:
                book_section = "book" + sections[1].split("movie")[0]
            else:
                book_section = """1. "Originals: How Non-Conformists Move the World" by Adam Grant
Explores how individuals who think creatively and challenge the status quo can make a significant impact on the world.

2. "Drive: The Surprising Truth About What Motivates Us" by Daniel H. Pink
Discusses what truly motivates people to excel, thrive, and contribute meaningfully in their work and personal lives.

3. "Daring Greatly: How the Courage to Be Vulnerable Transforms the Way We Live, Love, Parent, and Lead" by Brené Brown
Explores the power of vulnerability, courage, and connection in creating fulfilling relationships and embracing creativity."""
                
            sections = full_analysis.lower().split("movie")
            if len(sections) > 1:
                movie_section = "movie" + sections[1].split("music")[0]
            else:
                movie_section = """1. The Social Network
A fascinating exploration of ambition, innovation, and the interpersonal dynamics behind the creation of Facebook.

2. The Pursuit of Happyness
An inspiring true story about perseverance, resilience and maintaining hope in the face of overwhelming obstacles.

3. The Secret Life of Walter Mitty
A visually stunning film about breaking free from routine and finding courage to pursue adventure and meaningful experiences."""
                
            sections = full_analysis.lower().split("music")
            if len(sections) > 1:
                music_section = "music" + sections[1].split("relationship")[0]
            else:
                music_section = """1. "Vienna" by Billy Joel
A thoughtful reflection on taking time to appreciate life's journey rather than rushing through it.

2. "Here Comes the Sun" by The Beatles
An uplifting classic about optimism and the promise of better days ahead after difficult times.

3. "Weightless" by Marconi Union
A scientifically designed piece that promotes relaxation and mindfulness through its carefully crafted ambient sounds."""

            # Add this to the section where you extract data from the AI response
            sections = full_analysis.lower().split("celebrity")
            if len(sections) > 1:
                celebrity_section = "celebrity" + sections[1].split("relationship")[0]
            else:
                celebrity_section = """1. Emma Watson - Combines intelligence and analytical thinking with a passion for meaningful social causes.

            2. Benedict Cumberbatch - Exhibits a fascinating blend of intense focus, creative thinking, and deep curiosity about complex topics.

            3. Taylor Swift - Demonstrates meticulous attention to detail alongside expressive creativity and strategic planning abilities."""   
            sections = full_analysis.lower().split("relationship")
            if len(sections) > 1:
                relationship_section = "relationship" + sections[1].split("career")[0]
            else:
                relationship_section = """Strengths:
- Deep loyalty and commitment to partners
- Excellent communication and active listening skills
- Natural empathy and emotional understanding

Weaknesses:
- Tendency to overthink relationship dynamics
- Occasional need for reassurance and validation
- Difficulty addressing conflict directly"""
                
            sections = full_analysis.lower().split("career")
            if len(sections) > 1:
                career_section = "career" + sections[1]
            else:
                career_section = """Strengths:
- Exceptional analytical thinking and problem-solving abilities
- Careful attention to detail without losing sight of the big picture
- Creative approaches to challenges that others might miss

Ideal Career Paths:
- Research and data analysis in fields requiring innovative thinking
- Creative problem-solving roles in consulting or product development
- Strategic planning positions that benefit from nuanced perspectives"""
            
            # Store all data in session state
            st.session_state.personality_data = {
                "title": personality_title,
                "description": personality_desc,
                "profile": profile_text,
                "traits": personality_traits,
                "adjectives": trait_adjectives,
                "roast": personality_roast,
                "books": book_section,
                "movies": movie_section,
                "music": music_section,
                "celebrities": celebrity_section,
                "relationships": relationship_section,
                "career": career_section
            }
            
        except Exception as e:
            st.error(f"Something went wrong while generating the result: {str(e)}")
            if st.button("Try Again"):
                st.rerun()
            st.stop()

# Clean up recommendation sections to remove headers
def clean_recommendations(section):
    # Remove common headers
    section = section.replace("Books You Should Read:", "").replace("Recommended Books:", "")
    section = section.replace("Movies You Should Watch:", "").replace("Recommended Movies:", "")
    section = section.replace("Music You Should Listen To:", "").replace("Recommended Music:", "")
    section = section.replace("book recommendations:", "").replace("movie recommendations:", "").replace("music recommendations:", "")
    
    # Process numbered items and create structured format
    lines = section.strip().split('\n')
    result = []
    current_item = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line starts with a number or bullet
        if line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or line.startswith('-') or line.startswith('•'):
            # If we have a current item, add it to results
            if current_item:
                result.append(current_item)
                current_item = {}
            
            # Extract title part (before any description)
            parts = line.split('- ', 1) if '- ' in line else line.split(' • ', 1)
            if len(parts) > 1:
                title = parts[0].strip().lstrip('123.- •')
                description = parts[1].strip()
            else:
                # Handle case where description might be on next line
                title = line.strip().lstrip('123.- •')
                description = ""
                
            current_item = {"title": title, "description": description}
        elif current_item:
            # This is a continuation of the description
            current_item["description"] += " " + line
    
    # Add the last item if exists
    if current_item:
        result.append(current_item)
        
    return result

# Display results
data = st.session_state.personality_data

# Process recommendation sections
book_items = clean_recommendations(data['books'])
movie_items = clean_recommendations(data['movies'])
music_items = clean_recommendations(data['music'])

# Add main container for width control
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Instagram-inspired card layout
st.markdown('<div class="personality-title">The <strong>' + data['title'] + '</strong></div>', unsafe_allow_html=True)
st.markdown('<div class="personality-desc">' + data['description'] + '</div>', unsafe_allow_html=True)

# Main profile section with gradient border
st.markdown("""
<div class="instagram-gradient">
    <div class="instagram-gradient-inner">
        <div class="section-title"><span class="section-title-icon">👤</span> Your Personality Profile</div>
        <p style="font-size: 18px; line-height: 1.6;">{}</p>
    </div>
</div>
""".format(data['profile']), unsafe_allow_html=True)

# Replace your current roast section with this toggle version
if 'show_roast' not in st.session_state:
    st.session_state.show_roast = False

# Roast section with toggle button
st.markdown('<div class="roast-button-container" style="display: flex; justify-content: center; margin: 30px 0;">', unsafe_allow_html=True)
if st.button("🔥 " + ("Hide Roast" if st.session_state.get('show_roast', False) else "Roast Me"), key="roast_toggle"):
    st.session_state.show_roast = not st.session_state.get('show_roast', False)
    st.rerun()  # Force the page to refresh and update the button text
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get('show_roast', False):
    st.markdown(f'<div class="roast-content">{data["roast"]}</div>', unsafe_allow_html=True)

# Traits visualization section
st.markdown("<div class='section-title'><span class='section-title-icon'>📊</span> Your Personality Traits</div>", unsafe_allow_html=True)

# Create and display vertical bar chart
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
fig = create_vertical_bar_chart(data['traits'])
st.plotly_chart(fig, use_container_width=True)

# Display adjectives for each trait
for trait, adj_list in data['adjectives'].items():
    st.markdown(f"<div style='text-align: left; margin-bottom: 15px;'><b>{trait}:</b> <span style='color: #666; font-size: 16px;'>{', '.join(adj_list)}</span></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Books recommendations
st.markdown("<div class='section-title'><span class='section-title-icon'>📚</span> Books You Should Read</div>", unsafe_allow_html=True)
st.markdown("<div class='recommendation-container'>", unsafe_allow_html=True)

for item in book_items:
    st.markdown(f"""
    <div class="recommendation-item">
        <div class="recommendation-title">{item['title']}</div>
        <div class="recommendation-desc">{item['description']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Movies recommendations
st.markdown("<div class='section-title'><span class='section-title-icon'>🎬</span> Movies You Should Watch</div>", unsafe_allow_html=True)
st.markdown("<div class='recommendation-container'>", unsafe_allow_html=True)

for item in movie_items:
    st.markdown(f"""
    <div class="recommendation-item">
        <div class="recommendation-title">{item['title']}</div>
        <div class="recommendation-desc">{item['description']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Music recommendations
st.markdown("<div class='section-title'><span class='section-title-icon'>🎵</span> Music You Should Listen To</div>", unsafe_allow_html=True)
st.markdown("<div class='recommendation-container'>", unsafe_allow_html=True)

for item in music_items:
    st.markdown(f"""
    <div class="recommendation-item">
        <div class="recommendation-title">{item['title']}</div>
        <div class="recommendation-desc">{item['description']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Celebrity doppelgangers
st.markdown("<div class='section-title'><span class='section-title-icon'>🌟</span> Celebrity Doppelgangers</div>", unsafe_allow_html=True)
st.markdown("<div class='recommendation-container'>", unsafe_allow_html=True)

# Extract celebrity info using similar method as other recommendations
celebrity_items = clean_recommendations(data['celebrities'])

for item in celebrity_items:
    st.markdown(f"""
    <div class="recommendation-item">
        <div class="recommendation-title">{item['title']}</div>
        <div class="recommendation-desc">{item['description']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Process relationship and career insights
def process_insights(section, section_type):
    # Remove any headers
    section = section.replace(f"{section_type} Insights:", "").strip()
    
    # Initialize lists for different types of insights
    strengths = []
    weaknesses = []
    paths = []
    
    # Try to extract structured format first
    if "Strengths:" in section and ("Weaknesses:" in section or "Ideal Career Paths:" in section):
        # Extract strengths
        strengths_part = section.split("Strengths:")[1].split("Weaknesses:" if "Weaknesses:" in section else "Ideal Career Paths:")[0]
        for line in strengths_part.strip().split('\n'):
            clean_line = line.strip().lstrip('-').strip()
            if clean_line and len(clean_line) > 3:  # Ensure it's not just a bullet point
                strengths.append(clean_line)
        
        # Extract weaknesses
        if "Weaknesses:" in section:
            weaknesses_part = section.split("Weaknesses:")[1].split("Ideal Career Paths:" if "Ideal Career Paths:" in section else "\n\n")[0]
            for line in weaknesses_part.strip().split('\n'):
                clean_line = line.strip().lstrip('-').strip()
                if clean_line and len(clean_line) > 3:
                    weaknesses.append(clean_line)
        
        # Extract ideal career paths
        if "Ideal Career Paths:" in section:
            paths_part = section.split("Ideal Career Paths:")[1]
            for line in paths_part.strip().split('\n'):
                clean_line = line.strip().lstrip('-').strip()
                if clean_line and len(clean_line) > 3:
                    paths.append(clean_line)
    
    # If we couldn't extract structured data, provide default values
    if not strengths and section_type == "Relationship":
        strengths = ["Accepting", "Patient", "Authentic", "Observant"]
        weaknesses = ["Reserved", "Distant", "Self-conscious", "Passive"]
    elif not strengths and section_type == "Career":
        strengths = ["Analytical", "Determined", "Curious", "Focused"]
        paths = ["Creative problem-solver", "Technology specialist", "Research and development"]
        if not weaknesses:
            weaknesses = ["Perfectionist", "Restless", "Stubborn", "Hesitant"]
    
    return strengths, weaknesses, paths

# Relationship insights section with the new format
st.markdown("<div class='section-title'><span class='section-title-icon'>💝</span> Relationship Insights</div>", unsafe_allow_html=True)

rel_strengths, rel_weaknesses, _ = process_insights(data['relationships'], "Relationship")

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Summary</h3>", unsafe_allow_html=True)
st.markdown("<p>You gravitate towards intellectual pursuits and find comfort in structured, analytical environments. In relationships, you seek partners who can match your depth of curiosity while accepting your need for mental stimulation over physical activity. Your perfectionist tendencies extend beyond work into personal goals, but you maintain a healthy self-image despite acknowledging areas for improvement. Partners who appreciate both your technical mindset and creative outlets like photography tend to form the strongest connections with you.</p>", unsafe_allow_html=True)

st.markdown("<h3>Strengths and weaknesses</h3>", unsafe_allow_html=True)
st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 10px;'>", unsafe_allow_html=True)

for strength in rel_strengths:
    st.markdown(f"<div style='background-color: #e6f7e6; padding: 8px 16px; border-radius: 20px; font-weight: 600; color: #2e8b57; display: inline-block; margin-right: 8px; margin-bottom: 8px;'>{strength}</div>", unsafe_allow_html=True)

for weakness in rel_weaknesses:
    st.markdown(f"<div style='background-color: #ffebeb; padding: 8px 16px; border-radius: 20px; font-weight: 600; color: #d32f2f; display: inline-block; margin-right: 8px; margin-bottom: 8px;'>{weakness}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Career insights section with the new format
st.markdown("<div class='section-title'><span class='section-title-icon'>💼</span> Career Insights</div>", unsafe_allow_html=True)

career_strengths, career_weaknesses, career_paths = process_insights(data['career'], "Career")

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h3>Your workplace</h3>", unsafe_allow_html=True)
st.markdown("<p>In the world of careers, you thrive on cognitive challenges but resist structured physical activity, suggesting you seek mental rather than physical flow states. Creative problem-solving energizes you, whether it's cracking code or capturing moments through a lens. Those who work like you need constant intellectual stimulation and tend to dive deep into self-directed learning after hours.</p>", unsafe_allow_html=True)

st.markdown("<h3>Your perfect career</h3>", unsafe_allow_html=True)
st.markdown("<p>While you accept practical compromises for stability, you'll only find true fulfillment in roles that let you push boundaries and explore emerging technologies.</p>", unsafe_allow_html=True)

st.markdown("<h3>Strengths and weaknesses</h3>", unsafe_allow_html=True)
st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 10px;'>", unsafe_allow_html=True)

for strength in career_strengths:
    st.markdown(f"<div style='background-color: #e6f7e6; padding: 8px 16px; border-radius: 20px; font-weight: 600; color: #2e8b57; display: inline-block; margin-right: 8px; margin-bottom: 8px;'>{strength}</div>", unsafe_allow_html=True)

for weakness in career_weaknesses:
    st.markdown(f"<div style='background-color: #ffebeb; padding: 8px 16px; border-radius: 20px; font-weight: 600; color: #d32f2f; display: inline-block; margin-right: 8px; margin-bottom: 8px;'>{weakness}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Option to save or restart
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("📝 Download My Profile", use_container_width=True, key="download"):
        report_text = f"""# {data['title']}

{data['description']}

## Personality Profile
{data['profile']}

## Personality Traits
- Extraverted: {data['traits']['Extraverted']}% - {', '.join(data['adjectives']['Extraverted'])}
- Open: {data['traits']['Open']}% - {', '.join(data['adjectives']['Open'])}
- Conscientious: {data['traits']['Conscientious']}% - {', '.join(data['adjectives']['Conscientious'])}
- Agreeable: {data['traits']['Agreeable']}% - {', '.join(data['adjectives']['Agreeable'])}
- Neurotic: {data['traits']['Neurotic']}% - {', '.join(data['adjectives']['Neurotic'])}

## Books You Should Read
{data['books'].replace("Books You Should Read:", "").replace("Recommended Books:", "")}

## Movies You Should Watch
{data['movies'].replace("Movies You Should Watch:", "").replace("Recommended Movies:", "")}

## Music You Should Listen To
{data['music'].replace("Music You Should Listen To:", "").replace("Recommended Music:", "")}

## Relationship Insights
{data['relationships'].replace("Relationship Insights:", "")}

## Career Insights
{data['career'].replace("Career Insights:", "")}

## The Roast Section
{data['roast']}
"""
        st.download_button(
            label="Download as Text",
            data=report_text,
            file_name="my_personality_profile.txt",
            mime="text/plain",
            use_container_width=True
        )
with col2:
    if st.button("🔄 Start Over", use_container_width=True, key="restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("pages/1_Welcome.py")

# Footer
st.markdown("""
<div class="footer">
    © 2025 Personality Test
</div>
""".format(st.session_state.get('analysis_date', 'today')), unsafe_allow_html=True)

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
