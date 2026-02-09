import React, { useState } from 'react'
import Reader from './components/Reader/Reader'
import ReviewSession from './components/SRS/ReviewSession'
import { BookOpen, GraduationCap } from 'lucide-react'

function App() {
  const [view, setView] = useState('reader');
  const API_URL = "https://literate-winner-w9q56vpwjq6c549v-8000.app.github.dev";

  return (
    <div className="min-h-screen bg-slate-50 pb-20">
      {/* Navigation simple */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t flex justify-around py-3 z-50 shadow-2xl">
        <button 
          onClick={() => setView('reader')}
          className={`flex flex-col items-center ${view === 'reader' ? 'text-indigo-600' : 'text-slate-400'}`}
        >
          <BookOpen /> <span className="text-xs font-bold">Lire</span>
        </button>
        <button 
          onClick={() => setView('review')}
          className={`flex flex-col items-center ${view === 'review' ? 'text-indigo-600' : 'text-slate-400'}`}
        >
          <GraduationCap /> <span className="text-xs font-bold">Réviser</span>
        </button>
      </nav>

      {/* Contenu principal */}
      <main className="container mx-auto">
        {view === 'reader' ? (
          <Reader API_URL={API_URL} />
        ) : (
          <ReviewSession API_URL={API_URL} />
        )}
      </main>
    </div>
  )
}

export default App

