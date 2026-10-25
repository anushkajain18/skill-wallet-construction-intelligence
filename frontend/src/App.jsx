import React, { useState } from 'react';
import { Building2, ShieldCheck, Calculator, Bot, CloudSun, Upload, Github, PlayCircle, Activity, HardHat } from 'lucide-react';

const API = 'http://127.0.0.1:8000';
export default function App() {
  const [tab, setTab] = useState('overview');
  const [status, setStatus] = useState('');
  const [image, setImage] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [plan, setPlan] = useState({project_name:'Sample Construction Project',built_up_area_sqft:1200,floors:2,cost_per_sqft:1800,contingency_percent:10});
  const [planning, setPlanning] = useState(null);
  const [val, setVal] = useState({location:'Indore, Madhya Pradesh',area_sqft:1200,rate_per_sqft:3500,building_age_years:5,depreciation_percent_per_year:1});
  const [valuation, setValuation] = useState(null);
  const [question, setQuestion] = useState('What should I check before starting construction?');
  const [answer, setAnswer] = useState(null);
  const [weather, setWeather] = useState({weather:'rainy',activity:'concrete_pouring',temperature_c:28});
  const [advisory, setAdvisory] = useState(null);

  async function request(path, options={}) {
    setStatus('Working...');
    try {
      const res = await fetch(API + path, options);
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Request failed');
      setStatus('');
      return data;
    } catch (e) { setStatus(`Error: ${e.message}. Is the FastAPI backend running?`); return null; }
  }
  async function analyze(e) {
    e.preventDefault(); if (!image) return setStatus('Choose a construction image first.');
    const form = new FormData(); form.append('file', image); form.append('analysis_type', 'both');
    const data = await request('/api/analyze-image', {method:'POST', body:form}); if (data) setAnalysis(data);
  }
  async function runPlan(e) { e.preventDefault(); const d=await request('/api/planning',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...plan,built_up_area_sqft:Number(plan.built_up_area_sqft),floors:Number(plan.floors),cost_per_sqft:Number(plan.cost_per_sqft),contingency_percent:Number(plan.contingency_percent)})}); if(d)setPlanning(d); }
  async function runVal(e) { e.preventDefault(); const d=await request('/api/valuation',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...val,area_sqft:Number(val.area_sqft),rate_per_sqft:Number(val.rate_per_sqft),building_age_years:Number(val.building_age_years),depreciation_percent_per_year:Number(val.depreciation_percent_per_year)})}); if(d)setValuation(d); }
  async function ask(e) { e.preventDefault(); const d=await request('/api/assistant',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question})}); if(d)setAnswer(d); }
  async function runWeather(e) { e.preventDefault(); const d=await request('/api/weather-advisory',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...weather,temperature_c:Number(weather.temperature_c)})}); if(d)setAdvisory(d); }

  const nav = [
    ['overview','Overview',Building2],['safety','Image Analysis',ShieldCheck],['planning','Planning & Cost',Calculator],
    ['valuation','Valuation',Activity],['assistant','AI Assistant',Bot],['weather','Weather Advisory',CloudSun]
  ];
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-icon"><HardHat size={23}/></div><div><b>BuildWise AI</b><small>Construction Intelligence</small></div></div>
      <div className="nav-label">WORKSPACE</div>
      {nav.map(([id,label,Icon])=><button key={id} className={`nav-item ${tab===id?'active':''}`} onClick={()=>setTab(id)}><Icon size={18}/>{label}</button>)}
      <div className="sidebar-bottom"><span className="dot"/> Demo environment <small>v1.0 MVP</small></div>
    </aside>
    <main className="main">
      <header className="topbar"><div><span className="eyebrow">CAPSTONE PROJECT</span><h1>Multimodal Construction Intelligence Platform</h1><p>Safer sites. Smarter planning. Better decisions.</p></div><div className="avatar">BW</div></header>
      {status && <div className={status.startsWith('Error')?'alert error':'alert'}>{status}</div>}
      {tab==='overview' && <section>
        <div className="welcome"><div><span className="pill">AI-POWERED WORKSPACE</span><h2>Good work starts with better insight.</h2><p>Analyze site imagery, estimate project costs, plan tasks, and get construction guidance from one workspace.</p></div><div className="hero-icon"><Building2 size={66}/></div></div>
        <div className="stat-grid"><Stat icon={ShieldCheck} label="Safety & crack review" value="Image analysis" desc="Upload a site image"/><Stat icon={Calculator} label="Planning tools" value="Cost + schedule" desc="Estimate from your inputs"/><Stat icon={Bot} label="Assistant" value="Project guidance" desc="Ask a construction question"/></div>
        <h3 className="section-title">Project workflow</h3><div className="workflow">{[['01','Requirements','Define scope and inputs'],['02','Image analysis','Review safety and cracks'],['03','Planning & valuation','Estimate cost and value'],['04','AI advisory','Get contextual guidance'],['05','Testing & deployment','Validate and document']].map(x=><div className="workflow-card" key={x[0]}><span>{x[0]}</span><b>{x[1]}</b><small>{x[2]}</small></div>)}</div>
        <div className="note"><b>Prototype note</b><p>This capstone starter uses transparent demo logic. It does not yet connect a trained vision model, live weather feed, or external LLM.</p></div>
      </section>}
      {tab==='safety' && <section><PageTitle icon={ShieldCheck} title="Image-Based Analysis" subtitle="Upload a construction-site image for a structured review checklist."/><form className="panel" onSubmit={analyze}><label className="upload-box"><Upload size={28}/><b>{image?image.name:'Choose a site image'}</b><small>JPG, PNG, WEBP — maximum 10 MB</small><input type="file" accept="image/*" onChange={e=>setImage(e.target.files?.[0]||null)}/></label><button className="primary"><ShieldCheck size={17}/> Analyze image</button></form>{analysis&&<Result title="Analysis result"><p>{analysis.summary}</p>{analysis.findings.map((f,i)=><div className="finding" key={i}><b>{f.title}</b><span className="severity">{f.severity}</span><p>{f.description}</p><small>Recommended action: {f.recommended_action}</small></div>)}<p className="disclaimer">{analysis.disclaimer}</p></Result>}</section>}
      {tab==='planning' && <section><PageTitle icon={Calculator} title="Construction Planning & Cost" subtitle="Generate a rough schedule, material quantities, and budget estimate."/><form className="panel form-grid" onSubmit={runPlan}><Field label="Project name"><input value={plan.project_name} onChange={e=>setPlan({...plan,project_name:e.target.value})}/></Field><Field label="Area per floor (sq ft)"><input type="number" min="1" value={plan.built_up_area_sqft} onChange={e=>setPlan({...plan,built_up_area_sqft:e.target.value})}/></Field><Field label="Number of floors"><input type="number" min="1" value={plan.floors} onChange={e=>setPlan({...plan,floors:e.target.value})}/></Field><Field label="Cost per sq ft (₹)"><input type="number" min="1" value={plan.cost_per_sqft} onChange={e=>setPlan({...plan,cost_per_sqft:e.target.value})}/></Field><Field label="Contingency (%)"><input type="number" min="0" max="50" value={plan.contingency_percent} onChange={e=>setPlan({...plan,contingency_percent:e.target.value})}/></Field><button className="primary">Generate plan</button></form>{planning&&<Result title={planning.project_name}><div className="result-stats"><Metric label="Estimated total" value={money(planning.estimated_total_cost)}/><Metric label="Base cost" value={money(planning.estimated_base_cost)}/><Metric label="Duration" value={`${planning.estimated_duration_days} days`}/></div><h4>Approximate materials</h4><div className="material-grid">{Object.entries(planning.approximate_materials).map(([k,v])=><Metric key={k} label={k.replaceAll('_',' ')} value={v.toLocaleString()}/>)}</div><h4>Illustrative schedule</h4>{planning.schedule.map((t,i)=><div className="schedule-row" key={t.task}><span>{i+1}</span><b>{t.task}</b><small>{t.duration_days} days</small></div>)}<p className="disclaimer">{planning.assumptions.join(' ')}</p></Result>}</section>}
      {tab==='valuation' && <section><PageTitle icon={Activity} title="Real Estate Valuation" subtitle="Calculate an indicative value from area, rate, and age assumptions."/><form className="panel form-grid" onSubmit={runVal}><Field label="Location"><input value={val.location} onChange={e=>setVal({...val,location:e.target.value})}/></Field><Field label="Area (sq ft)"><input type="number" min="1" value={val.area_sqft} onChange={e=>setVal({...val,area_sqft:e.target.value})}/></Field><Field label="Rate per sq ft (₹)"><input type="number" min="1" value={val.rate_per_sqft} onChange={e=>setVal({...val,rate_per_sqft:e.target.value})}/></Field><Field label="Building age (years)"><input type="number" min="0" value={val.building_age_years} onChange={e=>setVal({...val,building_age_years:e.target.value})}/></Field><Field label="Depreciation per year (%)"><input type="number" min="0" max="10" value={val.depreciation_percent_per_year} onChange={e=>setVal({...val,depreciation_percent_per_year:e.target.value})}/></Field><button className="primary">Estimate value</button></form>{valuation&&<Result title="Valuation estimate"><div className="big-number">{money(valuation.estimated_value)}</div><p>Indicative value after {valuation.depreciation_percent}% assumed depreciation.</p><div className="schedule-row"><b>Gross value</b><span>{money(valuation.gross_value)}</span></div><p className="disclaimer">{valuation.note}</p></Result>}</section>}
      {tab==='assistant' && <section><PageTitle icon={Bot} title="Construction Assistant" subtitle="Ask general questions about site safety, cracks, materials, or project planning."/><form className="panel" onSubmit={ask}><Field label="Your question"><textarea rows="4" value={question} onChange={e=>setQuestion(e.target.value)}/></Field><button className="primary"><Bot size={17}/> Ask assistant</button></form>{answer&&<Result title="Assistant response"><p>{answer.answer}</p><h4>Suggested next steps</h4><ul>{answer.suggested_next_steps.map(s=><li key={s}>{s}</li>)}</ul><p className="disclaimer">{answer.disclaimer}</p></Result>}</section>}
      {tab==='weather' && <section><PageTitle icon={CloudSun} title="Weather-Aware Advisory" subtitle="Get a rule-based precaution list using weather and activity inputs."/><form className="panel form-grid" onSubmit={runWeather}><Field label="Weather"><select value={weather.weather} onChange={e=>setWeather({...weather,weather:e.target.value})}>{['sunny','hot','rainy','stormy','windy','unknown'].map(x=><option key={x}>{x}</option>)}</select></Field><Field label="Construction activity"><select value={weather.activity} onChange={e=>setWeather({...weather,activity:e.target.value})}>{[['general','General'],['concrete_pouring','Concrete pouring'],['roof_work','Roof work'],['painting','Painting'],['excavation','Excavation']].map(([v,l])=><option key={v} value={v}>{l}</option>)}</select></Field><Field label="Temperature (°C)"><input type="number" value={weather.temperature_c} onChange={e=>setWeather({...weather,temperature_c:e.target.value})}/></Field><button className="primary">Get advisory</button></form>{advisory&&<Result title="Site advisory"><span className={`risk ${advisory.risk_level}`}>{advisory.risk_level.toUpperCase()} RISK</span><ul>{advisory.recommendations.map(s=><li key={s}>{s}</li>)}</ul><p className="disclaimer">{advisory.note}</p></Result>}</section>}
      <footer><span>BuildWise AI · Capstone MVP</span><span>Demo data · Verify professional decisions</span></footer>
    </main>
  </div>;
}
function Stat({icon:Icon,label,value,desc}) { return <div className="stat-card"><div className="stat-icon"><Icon size={20}/></div><small>{label}</small><b>{value}</b><span>{desc}</span></div>; }
function PageTitle({icon:Icon,title,subtitle}) { return <div className="page-title"><div className="title-icon"><Icon size={24}/></div><div><h2>{title}</h2><p>{subtitle}</p></div></div>; }
function Field({label,children}) { return <label className="field"><span>{label}</span>{children}</label>; }
function Result({title,children}) { return <div className="panel result"><h3>{title}</h3>{children}</div>; }
function Metric({label,value}) { return <div className="metric"><small>{label}</small><b>{value}</b></div>; }
function money(n) { return new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:0}).format(n||0); }
