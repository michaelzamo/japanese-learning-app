import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { CheckCircle, XCircle, AlertCircle, RefreshCw } from 'lucide-react';

const ReviewSession = ({ API_URL }) => {
  const [queue, setQueue] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/reviews`);
      setQueue(response.data);
    } catch (error) {
      console.error("Erreur lors du chargement des révisions", error);
    } finally {
      setLoading(false);
    }
  };

  const handleRate = async (quality) => {
    const currentCard = queue[currentIndex];
    try {
      await axios.post(`${API_URL}/api/reviews/${currentCard.id}?quality=${quality}`);
      
      // Passer à la carte suivante
      if (currentIndex < queue.length - 1) {
        setCurrentIndex(currentIndex + 1);
        setShowAnswer(false);
      } else {
        setQueue([]); // Session terminée
      }
    } catch (error) {
      alert("Erreur lors de la mise à jour du SRS");
    }
  };

  if (loading) return <div className="text-center p-10"><RefreshCw className="animate-spin mx-auto" /> Chargement...</div>;
  
  if (queue.length === 0) return (
    <div className="text-center p-10 bg-white rounded-2xl shadow-sm border">
      <CheckCircle className="text-emerald-500 w-16 h-16 mx-auto mb-4" />
      <h2 className="text-2xl font-bold">Félicitations !</h2>
      <p className="text-slate-500">Vous avez révisé tous vos mots pour aujourd'hui.</p>
      <button onClick={fetchReviews} className="mt-4 text-indigo-600 hover:underline">Vérifier à nouveau</button>
    </div>
  );

  const card = queue[currentIndex];

  return (
    <div className="max-w-xl mx-auto mt-10 p-4">
      <div className="mb-4 flex justify-between text-sm text-slate-400 font-medium">
        <span>Progression : {currentIndex + 1} / {queue.length}</span>
        <span>Mode Révision</span>
      </div>

      <div className="bg-white min-h-[400px] rounded-3xl shadow-xl border-t-8 border-indigo-500 p-8 flex flex-col justify-between transition-all">
        {/* RECTO : Le mot et le contexte */}
        <div className="text-center space-y-8">
          <div className="text-6xl font-bold text-slate-800 mb-4">{card.word_text}</div>
          
          <div className="bg-slate-50 p-6 rounded-2xl italic text-slate-600 text-lg border-l-4 border-indigo-300">
            {/* On peut mettre le mot en gras dans la phrase de contexte */}
            "{card.context_sentence}"
          </div>
        </div>

        {/* VERSO : La réponse (cachée par défaut) */}
        {showAnswer ? (
          <div className="animate-in fade-in zoom-in duration-300 space-y-6">
            <div className="text-center border-t pt-6">
              <p className="text-2xl text-indigo-600 font-bold">{card.reading}</p>
              <p className="text-slate-500 mt-2">{card.definition}</p>
            </div>

            <div className="grid grid-cols-3 gap-3">
              <button onClick={() => handleRate('forgot')} className="flex flex-col items-center p-3 bg-red-50 text-red-600 rounded-xl hover:bg-red-100 transition">
                <XCircle size={24} /> <span className="text-xs mt-1 font-bold">Oublié</span>
              </button>
              <button onClick={() => handleRate('hard')} className="flex flex-col items-center p-3 bg-orange-50 text-orange-600 rounded-xl hover:bg-orange-100 transition">
                <AlertCircle size={24} /> <span className="text-xs mt-1 font-bold">Difficile</span>
              </button>
              <button onClick={() => handleRate('easy')} className="flex flex-col items-center p-3 bg-emerald-50 text-emerald-600 rounded-xl hover:bg-emerald-100 transition">
                <CheckCircle size={24} /> <span className="text-xs mt-1 font-bold">Facile</span>
              </button>
            </div>
          </div>
        ) : (
          <button 
            onClick={() => setShowAnswer(true)}
            className="w-full py-4 bg-indigo-600 text-white rounded-2xl font-bold text-xl hover:bg-indigo-700 shadow-lg transition-transform active:scale-95"
          >
            Afficher la réponse
          </button>
        )}
      </div>
    </div>
  );
};

export default ReviewSession;
