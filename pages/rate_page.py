import streamlit as st
from custom import top_menu, bottom_head

top_menu()


# System usability scale - SUS questionaire function
def SUS():
    with st.form("quest1"):
        res = [1, 2, 3, 4, 5]

        a = st.radio("I think that I would like to use this system frequently.", res, horizontal=True)
        b = st.radio("I found the system unnecessarily complex.", res, horizontal=True)
        c = st.radio("I thought the system was easy to use.", res, horizontal=True)
        d = st.radio("I think that I would need the support of a technical person to be able to use this system.", res, horizontal=True)
        e = st.radio("I found the various functions in this system were well integrated.", res, horizontal=True)
        f = st.radio("I thought there was too much inconsistency in this system.", res, horizontal=True)
        g = st.radio("I would imagine that most people would learn to use this system very quickly.", res, horizontal=True)
        h = st.radio("I found the system very cumbersome to use.", res, horizontal=True)
        i = st.radio("I felt very confident using the system.", res, horizontal=True)
        j = st.radio("I needed to learn a lot of things before I could get going with this system.", res, horizontal=True)

        pos = a+c+e+g+i-5
        neg = b+d+f+h+j-25
        result = 2.5*(pos-neg)

        st.write("Total:", result)

        submitted = st.form_submit_button()

        return submitted


def quest2():
    res = [1, 2, 3, 4, 5]

    a = st.radio("Rate1", res, horizontal=True)

    b = st.radio("Rate2", res, horizontal=True)

    st.write("Total:", a+b)



def quest3():
    res = [1, 2, 3, 4, 5]

    a = st.radio("Rate1", res, horizontal=True)

    b = st.radio("Rate2", res, horizontal=True)

    st.write("Total:", a+b)

quest_opts = [" ", "System usability scale - SUS", "Quest2", "Quest3"]

quest_out = st.selectbox("Which questionaire?", quest_opts)

# form
match quest_out:
    case "System usability scale - SUS":
        sub = SUS()
    case "Quest2":
        sub = quest2()
    case "Quest3":
        sub = quest3()
    case _:
        st.write("Choose a questionaire type")
        sub = False


bottom_head()
