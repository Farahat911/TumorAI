import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useParams } from 'react-router-dom';

function Home({ reports }) {
  const [searchTerm, setSearchTerm] = useState('');

  const stats = {
    total: reports.length,
    critical: reports.filter(r => r.data.severity_level >= 3).length,
    stable: reports.filter(r => r.data.severity_level < 3).length
  };

  const filteredReports = reports.filter(r => 
    r.caseName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getSeverityBadge = (level) => {
    if (level === 1) return { text: 'يستجيب للعلاج', bg: 'var(--success-bg)', color: 'var(--success-text)', border: '#059669' };
    if (level === 2) return { text: 'مستقر / متابعة', bg: '#332919', color: '#fbbf24', border: '#b45309' };
    if (level === 3) return { text: 'مؤشر خطر', bg: '#431407', color: '#fb923c', border: '#c2410c' };
    return { text: 'تدخل فوري', bg: 'var(--danger-bg)', color: 'var(--danger-text)', border: 'var(--danger-border)' };
  };

  return (
    <div className="app-container">
      <div className="main-header">
        {/* التعديل هنا: كبرنا اللوجو لـ 150px وضفنا Shadow أزرق شيك */}
        <img src="/logo.png" alt="شعار" style={{ 
          width: '150px', 
          borderRadius: '20px', 
          marginBottom: '20px',
          filter: 'drop-shadow(0 0 15px rgba(59, 130, 246, 0.5))' 
        }} />
        <h1>لوحة التحكم الطبية | TumorAI</h1>
        <p>نظام ذكاء اصطناعي متكامل لتحليل نمو وتصنيف الأورام الجلدية</p>
      </div>

      <div className="stats-grid" style={{ marginBottom: '30px' }}>
        <div className="stat-box highlight">
          <div style={{fontSize: '0.9rem', opacity: 0.8}}>إجمالي الحالات</div>
          <div style={{fontSize: '2rem', fontWeight: 'bold'}}>{stats.total}</div>
        </div>
        <div className="stat-box" style={{border: '1px solid #c2410c', background: '#431407'}}>
          <div style={{fontSize: '0.9rem', color: '#fb923c'}}>حالات حرجة (AI)</div>
          <div style={{fontSize: '2rem', fontWeight: 'bold', color: '#fb923c'}}>{stats.critical}</div>
        </div>
        <div className="stat-box" style={{border: '1px solid #059669', background: 'var(--success-bg)'}}>
          <div style={{fontSize: '0.9rem', color: 'var(--success-text)'}}>حالات مستقرة</div>
          <div style={{fontSize: '2rem', fontWeight: 'bold', color: 'var(--success-text)'}}>{stats.stable}</div>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '15px', marginBottom: '25px', alignItems: 'center' }}>
        <input 
          type="text" 
          className="form-input" 
          placeholder="🔍 ابحث عن مريض بالاسم..." 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{ flex: 1, margin: 0 }}
        />
        <Link to="/new" className="btn btn-primary" style={{ whiteSpace: 'nowrap' }}>+ فحص جديد</Link>
      </div>

      {filteredReports.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '50px' }}>
          <h3 style={{ color: 'var(--text-muted)' }}>لا توجد نتائج مطابقة لبحثك</h3>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '15px' }}>
          {filteredReports.map((report) => {
            const badge = getSeverityBadge(report.data.severity_level);
            return (
              <div key={report.id} className="card card-hover" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3 style={{ margin: '0 0 8px 0', color: 'var(--text-main)' }}>{report.caseName}</h3>
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>📅 {report.date}</span>
                    <span style={{ color: badge.color, fontSize: '12px', fontWeight: 'bold' }}>🩺 {badge.text}</span>
                  </div>
                </div>
                <Link to={`/report/${report.id}`} className="btn btn-secondary">الملف الطبي</Link>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function NewAnalysis({ onSave }) {
  const [caseName, setCaseName] = useState('');
  const [files, setFiles] = useState([null, null, null, null]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (index, event) => {
    const newFiles = [...files];
    newFiles[index] = event.target.files[0];
    setFiles(newFiles);
  };

  const handleAnalyze = async () => {
    if (!caseName.trim()) return alert("برجاء إدخال اسم المريض.");
    const validFiles = files.filter(file => file !== null);
    if (validFiles.length === 0) return alert("برجاء رفع صورة واحدة على الأقل.");

    setLoading(true);
    const formData = new FormData();
    validFiles.forEach(file => formData.append("files", file));

    try {
      // تعديل مسار الـ API ليكون POST ويرسل الصور فعلياً
      const res = await fetch("http://127.0.0.1:8000/api/analyze-images", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      
      const newReport = {
        id: Date.now().toString(),
        caseName: caseName,
        date: new Date().toLocaleDateString('ar-EG'),
        data: data
      };
      
      await onSave(newReport);
      navigate(`/report/${newReport.id}`);
    } catch (error) {
      alert("حدث خطأ في الاتصال بالسيرفر.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div style={{ marginBottom: '30px' }}>
        <Link to="/" style={{color: 'var(--primary)', textDecoration: 'none'}}>← العودة للوحة التحكم</Link>
        <h2 style={{ marginTop: '10px' }}>إجراء فحص Deep Learning جديد</h2>
      </div>

      <div className="card">
        <div className="form-group">
          <label className="form-label">اسم المريض:</label>
          <input type="text" className="form-input" value={caseName} onChange={(e) => setCaseName(e.target.value)} placeholder="أدخل الاسم الرباعي" />
        </div>

        <div style={{ marginTop: '20px' }}>
          <label className="form-label">صور المتابعة (يرجى رفع الصور بالترتيب الزمني):</label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginTop: '15px' }}>
            {files.map((_, index) => (
              <div key={index} className="stat-box" style={{padding: '10px', textAlign: 'right'}}>
                <label style={{fontSize: '12px', display: 'block', marginBottom: '5px'}}>الأسبوع {index + 1}</label>
                <input type="file" accept="image/*" onChange={(e) => handleFileChange(index, e)} style={{fontSize: '11px', width: '100%'}} />
              </div>
            ))}
          </div>
        </div>
        
        <button onClick={handleAnalyze} disabled={loading} className="btn btn-primary" style={{ width: '100%', marginTop: '30px', padding: '18px', fontSize: '1.1rem' }}>
          {loading ? '⏳ جاري تشغيل الشبكة العصبية...' : '🚀 بدء التحليل واستخراج النتائج'}
        </button>
      </div>
    </div>
  );
}

function ReportView({ reports }) {
  const { id } = useParams();
  const reportWrapper = reports.find(r => r.id === id);
  if (!reportWrapper) return <div className="app-container"><h3>التقرير غير موجود.</h3></div>;

  const report = reportWrapper.data;
  const isMalignant = report.ai_classification.includes('خبيث');
  const confidenceScore = report.ai_classification.match(/(\d+\.?\d*)%/)?.[1] || 0;

  return (
    <div className="app-container report-print">
      <div className="no-print" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <Link to="/" className="btn btn-secondary">← السجل</Link>
        <button onClick={() => window.print()} className="btn btn-primary" style={{background: '#059669'}}>طباعة تقرير طبي PDF</button>
      </div>

      <div className="card" style={{ borderTop: `8px solid ${isMalignant ? '#ef4444' : '#10b981'}`, padding: '40px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '2px solid var(--border-color)', paddingBottom: '20px', marginBottom: '30px' }}>
           <div>
              <h1 style={{margin: 0, color: 'var(--primary)'}}>TumorAI Report</h1>
              <p style={{margin: '5px 0 0 0', opacity: 0.7}}>نظام التشخيص المبكر المدعوم بالذكاء الاصطناعي</p>
           </div>
           <div style={{textAlign: 'left', direction: 'ltr'}}>
              <div style={{fontWeight: 'bold'}}>ID: {reportWrapper.id}</div>
              <div>Date: {reportWrapper.date}</div>
           </div>
        </div>

        <div style={{marginBottom: '30px'}}>
            <h3 style={{borderRight: '4px solid var(--primary)', paddingRight: '10px'}}>بيانات المريض: {reportWrapper.caseName}</h3>
        </div>

        <div className="stat-box" style={{background: '#020617', padding: '30px', marginBottom: '30px'}}>
            <h4 style={{marginTop: 0, color: 'var(--text-muted)'}}>قرار نظام التعلم العميق:</h4>
            <div style={{fontSize: '1.8rem', fontWeight: 'bold', color: isMalignant ? '#f87171' : '#34d399', marginBottom: '15px'}}>
                {report.ai_classification.split(' (')[0]}
            </div>
            
            <div style={{display: 'flex', alignItems: 'center', gap: '15px'}}>
                <div style={{flex: 1, height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '10px'}}>
                    <div style={{width: `${confidenceScore}%`, height: '100%', background: isMalignant ? '#ef4444' : '#10b981', borderRadius: '10px'}}></div>
                </div>
                <span style={{fontWeight: 'bold'}}>{confidenceScore}% الثقة</span>
            </div>
        </div>

        <div className="stats-grid" style={{marginBottom: '30px'}}>
            <div className="stat-box">
                <div style={{color: 'var(--text-muted)'}}>معدل النمو</div>
                <div style={{fontSize: '1.5rem', fontWeight: 'bold', direction: 'ltr'}}>{report.average_growth_rate}%</div>
            </div>
            <div className="stat-box">
                <div style={{color: 'var(--text-muted)'}}>درجة الخطورة</div>
                <div style={{fontSize: '1.5rem', fontWeight: 'bold'}}>{report.severity_level} / 4</div>
            </div>
        </div>

        <div style={{marginBottom: '30px'}}>
            <h4 style={{color: 'var(--text-muted)'}}>التشخيص والمتابعة:</h4>
            <p style={{fontSize: '1.2rem', lineHeight: '1.6'}}>{report.diagnosis}</p>
        </div>

        <h4>الصور التحليلية (Visual Analysis):</h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '15px' }}>
            {report.extracted_areas.map((area, idx) => (
                <div key={idx} style={{textAlign: 'center'}}>
                    {report.processed_images && report.processed_images[idx] && <img src={report.processed_images[idx]} style={{width: '100%', borderRadius: '10px', border: '1px solid var(--border-color)'}} />}
                    <div style={{marginTop: '5px', fontWeight: 'bold'}}>{area} mm²</div>
                    <div style={{fontSize: '12px', opacity: 0.6}}>أسبوع {idx+1}</div>
                </div>
            ))}
        </div>

        <div style={{marginTop: '50px', paddingTop: '20px', borderTop: '1px solid var(--border-color)', fontSize: '12px', textAlign: 'center', opacity: 0.5}}>
            هذا التقرير تم إنشاؤه آلياً بواسطة نظام TumorAI. يجب مراجعة النتائج من قبل طبيب مختص.
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/reports")
      .then(res => res.json())
      .then(data => setReports(data))
      .catch(err => console.error("Error fetching:", err));
  }, []);

  const handleSaveReport = async (newReport) => {
    try {
      await fetch("http://127.0.0.1:8000/api/reports", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newReport)
      });
      setReports([newReport, ...reports]);
    } catch(e) { console.error("Error saving:", e); }
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home reports={reports} />} />
        <Route path="/new" element={<NewAnalysis onSave={handleSaveReport} />} />
        <Route path="/report/:id" element={<ReportView reports={reports} />} />
      </Routes>
    </Router>
  );
}