import time
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Federated Lab | Israel", page_icon="🛰️", layout="wide")

RUN_ID = "71136882943249323"
rounds = pd.DataFrame({
    "Round": [0, 1, 2, 3],
    "Global Accuracy": [9.61, 28.90, 39.54, 44.56],
    "Global Loss": [2.3055, 1.9486, 1.6549, 1.5076],
})
clients = pd.DataFrame({
    "Client": ["Client 1", "Client 2", "Client 3"],
    "Eval Accuracy (%)": [43.88, 28.43, 43.25],
    "Eval Loss": [1.5278, 1.9552, 1.5459],
    "Recorded Steps": [3, 1, 3],
})

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
.stApp{background:radial-gradient(circle at 80% 0%,#17364a 0,#071522 48%,#06111c 100%);color:#eaf2f7}
html,body,[class*="css"]{font-family:'Manrope',sans-serif}
.block-container{padding-top:1.6rem;max-width:1500px}
section[data-testid="stSidebar"]{background:#0b1c2a;border-right:1px solid #24465a}
.hero{padding:1.4rem 1.6rem;border:1px solid #24465a;border-radius:20px;background:linear-gradient(120deg,#143649,#0b1f2f)}
.eyebrow{color:#65d6c5;font:500 .72rem 'DM Mono',monospace;letter-spacing:.16em}
.hero-title{font-size:2rem;font-weight:800;color:#f3f8fb;margin:.3rem 0}
.sub{color:#a9bdca;font-size:.9rem}
.kpi{background:linear-gradient(145deg,#142f43,#0d2233);border:1px solid #24465a;border-radius:16px;padding:1rem;min-height:105px}
.klabel{color:#9ab0bf;font:500 .7rem 'DM Mono',monospace;letter-spacing:.08em}
.kvalue{color:#f2f7fa;font-size:1.8rem;font-weight:800;margin-top:.25rem}
.section{font-size:1.08rem;font-weight:800;color:#eaf2f7;margin:.5rem 0 .15rem}
.note{color:#8fa7b7;font-size:.78rem;margin-bottom:.8rem}
div.stButton>button{border-radius:12px;border:1px solid #65d6c5;background:linear-gradient(90deg,#176d70,#1c8a83);color:white;font-weight:800;padding:.65rem}
[data-testid="stMetric"]{background:#102638;border:1px solid #24465a;padding:1rem;border-radius:14px}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="eyebrow">FEDERATION CONSOLE</div>', unsafe_allow_html=True)
    st.title("Israel's Lab")
    st.caption("Flower · PyTorch · FedAvg")
    st.divider()
    st.markdown("**Run ID**")
    st.code(RUN_ID)
    st.markdown("**Architecture**")
    st.write("🖥️  1 Server")
    st.write("🧩  3 virtual Clients")
    st.write("🔄  3 training rounds")
    st.write("🧠  CIFAR-10")
    st.divider()
    st.success("Recorded run loaded")
    st.caption("Animation is a visual replay, not a new training job.")

st.markdown(f"""
<div class="hero">
 <div class="eyebrow">DISTRIBUTED INTELLIGENCE / EXPERIMENT 01</div>
 <div class="hero-title">FEDERATED LAB <span style="color:#65d6c5">/</span> CONTROL CENTER</div>
 <div class="sub">A command deck for server coordination, client training and FedAvg aggregation.</div>
 <div style="margin-top:1rem"><span style="border:1px solid #36786f;background:#123d3b;color:#8ce5d7;border-radius:999px;padding:.35rem .75rem;font:500 .72rem 'DM Mono',monospace">● COMPLETED RUN · {RUN_ID}</span></div>
</div>
""", unsafe_allow_html=True)

st.write("")
cols = st.columns(4)
for c, label, val, note in zip(cols,
    ["GLOBAL ACCURACY","GLOBAL LOSS","CLIENT NODES","FEDAVG ROUNDS"],
    ["44.56%","1.5076","03","03 / 03"],
    ["Server · final evaluation","Server · final evaluation","All clients trained each round","Strategy completed"]):
    c.markdown(f'<div class="kpi"><div class="klabel">{label}</div><div class="kvalue">{val}</div><div class="note">{note}</div></div>',unsafe_allow_html=True)

def topology(phase="idle", progress=0.0, round_no=0, active=0):
    sx, sy = .5, .82
    coords = [(.16,.18),(.5,.18),(.84,.18)]
    fig = go.Figure()
    for i,(x,y) in enumerate(coords):
        on = phase != "idle" and (active == i or phase == "aggregate")
        fig.add_trace(go.Scatter(x=[sx,x],y=[sy,y],mode="lines",
            line=dict(color="#65d6c5" if on else "#547286",width=3 if on else 1.7),
            hoverinfo="skip",showlegend=False))
        fig.add_trace(go.Scatter(x=[x],y=[y],mode="markers+text",
            marker=dict(size=48,color="#1b6d70" if on else "#173b50",
                        line=dict(color="#f2a66d" if on else "#52758a",width=2)),
            text=[f"C{i+1}"],textposition="middle center",
            textfont=dict(color="white",size=13),hovertemplate=f"Client {i+1}<extra></extra>",showlegend=False))
    fig.add_trace(go.Scatter(x=[sx],y=[sy],mode="markers+text",
        marker=dict(size=62,color="#176d70",line=dict(color="#65d6c5",width=3)),
        text=["SERVER"],textposition="middle center",textfont=dict(color="white",size=11),showlegend=False))
    if phase in ("broadcast","upload"):
        x0,y0=coords[active]
        if phase=="broadcast":
            x,y=sx+(x0-sx)*progress,sy+(y0-sy)*progress
            col="#65d6c5"
        else:
            x,y=x0+(sx-x0)*progress,y0+(sy-y0)*progress
            col="#f2a66d"
        fig.add_trace(go.Scatter(x=[x],y=[y],mode="markers",
            marker=dict(size=18,color=col,line=dict(color="white",width=2)),showlegend=False,hoverinfo="skip"))
    fig.update_layout(height=370,margin=dict(l=5,r=5,t=12,b=5),
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False,range=[0,1]),yaxis=dict(visible=False,range=[.03,1]),
        annotations=[dict(x=.5,y=.99,text=f"SERVER · GLOBAL MODEL · ROUND {round_no}/3" if round_no else "SERVER · GLOBAL MODEL",
        showarrow=False,font=dict(color="#9ab0bf",size=10)),
        dict(x=.5,y=.02,text="CLIENT NODES · LOCAL DATA PARTITIONS",showarrow=False,font=dict(color="#9ab0bf",size=9))])
    return fig

left,right=st.columns([1.25,1],gap="large")
with left:
    st.markdown('<div class="section">Federation topology</div><div class="note">One coordinator connected to three simulated client nodes.</div>',unsafe_allow_html=True)
    graph=st.empty()
    status=st.empty()
    graph.plotly_chart(topology(),use_container_width=True,config={"displayModeBar":False})
    b1,b2=st.columns(2)
    run=b1.button("▶ START VISUAL REPLAY",use_container_width=True)
    reset=b2.button("↺ RESET VIEW",use_container_width=True)
    if reset:
        graph.plotly_chart(topology(),use_container_width=True,config={"displayModeBar":False})
        status.info("Topology reset. Ready to replay the recorded run.")
    if run:
        events=[]
        for r in range(1,4):
            for i in range(3): events.append((r,"broadcast",i,f"Server broadcasts global model to Client {i+1}"))
            for i in range(3): events.append((r,"upload",i,f"Client {i+1} returns its local model update"))
            events.append((r,"aggregate",0,f"Server aggregates Round {r} using FedAvg"))
        bar=st.progress(0,text="Preparing federation replay...")
        for n,(r,p,i,msg) in enumerate(events):
            if p=="aggregate":
                graph.plotly_chart(topology("idle",0,r),use_container_width=True,config={"displayModeBar":False})
                status.success(f"ROUND {r} · {msg}")
                time.sleep(.4)
            else:
                for f in range(11):
                    graph.plotly_chart(topology(p,f/10,r,i),use_container_width=True,config={"displayModeBar":False})
                    status.info(f"ROUND {r} · {msg}")
                    time.sleep(.045)
            bar.progress((n+1)/len(events),text=f"Replaying federation events · {n+1}/{len(events)}")
        bar.empty()
        status.success("✓ Replay complete · 3 clients · 3 FedAvg rounds.")

with right:
    st.markdown('<div class="section">Global model performance</div><div class="note">Actual Server-side evaluation from the completed Flower run.</div>',unsafe_allow_html=True)
    fa=px.line(rounds,x="Round",y="Global Accuracy",markers=True)
    fa.update_traces(line=dict(color="#65d6c5",width=4),marker=dict(size=10,color="#65d6c5"))
    fa.update_layout(height=190,margin=dict(l=5,r=5,t=5,b=5),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#c6d6df",xaxis=dict(title="Round",gridcolor="#24465a",dtick=1),yaxis=dict(title="Accuracy (%)",gridcolor="#24465a",range=[0,55]))
    st.plotly_chart(fa,use_container_width=True,config={"displayModeBar":False})
    fl=px.line(rounds,x="Round",y="Global Loss",markers=True)
    fl.update_traces(line=dict(color="#f2a66d",width=4),marker=dict(size=10,color="#f2a66d"))
    fl.update_layout(height=190,margin=dict(l=5,r=5,t=5,b=5),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#c6d6df",xaxis=dict(title="Round",gridcolor="#24465a",dtick=1),yaxis=dict(title="Loss",gridcolor="#24465a"))
    st.plotly_chart(fl,use_container_width=True,config={"displayModeBar":False})

st.write("")
st.markdown('<div class="section">Client diagnostics</div><div class="note">Local TensorBoard evaluation metrics. Client 2 has one recorded step only; missing steps are not invented.</div>',unsafe_allow_html=True)
a,b=st.columns([1.05,1],gap="large")
with a:
    fc=px.bar(clients,x="Client",y="Eval Accuracy (%)",color="Client",text="Eval Accuracy (%)",color_discrete_sequence=["#65d6c5","#f2a66d","#82a9ff"])
    fc.update_traces(texttemplate="%{text:.2f}%",textposition="outside")
    fc.update_layout(height=300,margin=dict(l=5,r=5,t=15,b=5),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#c6d6df",yaxis=dict(title="Accuracy (%)",gridcolor="#24465a",range=[0,55]),xaxis=dict(title=""),showlegend=False)
    st.plotly_chart(fc,use_container_width=True,config={"displayModeBar":False})
with b:
    st.dataframe(clients,hide_index=True,use_container_width=True,height=250)
    st.caption("Client 1 and 3: 3 steps. Client 2: 1 step.")

st.write("")
st.markdown('<div class="section">Round-by-round server report</div><div class="note">Global evaluation before training and after each FedAvg round.</div>',unsafe_allow_html=True)
st.dataframe(rounds,hide_index=True,use_container_width=True)

with st.expander("Experiment details & interpretation"):
    st.markdown("""
    - Framework: Flower 1.39.0
    - App: `@flwrlabs/custom-mods` version 1.1.11
    - Algorithm: Federated Averaging (FedAvg)
    - Dataset/model: CIFAR-10 with the template's PyTorch model
    - Federation: 1 Server and 3 simulated SuperNodes
    - Rounds: 3
    - Final model: `final_model.pt`
    - Monitoring logs: `.runs_history`

    The topology animation is a visual replay of the recorded workflow. It illustrates model broadcast, client updates and server aggregation; it does not launch another Flower training run.
    """)
st.caption("ISRAEL · FEDERATED LEARNING PROJECT · SOURCE: FLOWER RUN " + RUN_ID)

