import { useState } from 'react';
import './App.css';
import UploadTab from './components/UploadTab';
import HistoryTab from './components/HistoryTab';

function App() {
  // State to keep track of the current active tab. Defaults to 'upload'.
  const [activeTab, setActiveTab] = useState('upload');

  return (
    <div className="App">
      {/* Standard header for the application */}
      <header className="App-header">
        <h1>Smart Resume Analyzer</h1>
        <p>Get AI-powered feedback on your resume instantly</p>
      </header>

      {/* Navigation controls to switch between tabs */}
      <nav className="App-nav">
        <button
          className={activeTab === 'upload' ? 'active' : ''}
          onClick={() => setActiveTab('upload')}
        >
          Upload Resume
        </button>
        <button
          className={activeTab === 'history' ? 'active' : ''}
          onClick={() => setActiveTab('history')}
        >
          View History
        </button>
      </nav>

      {/* Main content area where the active tab's component is shown */}
      <main className="App-main">
        <div style={{ display: activeTab === 'upload' ? 'block' : 'none' }}>
          <UploadTab />
        </div>
        <div style={{ display: activeTab === 'history' ? 'block' : 'none' }}>
          <HistoryTab active={activeTab === 'history'} />
        </div>
      </main>
    </div>
  );
}

export default App;