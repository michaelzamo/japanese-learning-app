import React, { useState } from 'react';
import axios from 'axios';


const Reader = ({ API_URL }) => {
  const [inputText, setInputText] = useState("");
  const [tokens, setTokens] = useState([]);
  const [selectedWord, setSelectedWord] = useState(null);
  const [contextSentence, setContextSentence] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const analyzeText = async () => {
    setIsAnalyzing(true);
    try {
      const response = await axios.post(`${API_URL}/api/test-nlp`, { text: inputText });
      setTokens(response.data.tokens);
    } catch (error) {
      alert("Erreur");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleWordClick = (token, index) => {
    setSelectedWord(token);
    
    // Logique d'extraction de la phrase (on cherche les limites comme '。', '！', '？')
    let start = index;
    while (start > 0 && !['。', '！', '？', '\n'].includes(tokens[start - 1].surface)) {
      start--;
    }
    
    let end = index;
    while (end < tokens.length - 1 && !['。', '！', '？', '\n'].includes(tokens[end].surface)) {
      end++;
    }
    
    const sentence = tokens.slice(start, end + 1).map(t => t.surface).join("");
    setContextSentence(sentence);
  };


  const saveWord = async () => {
    try {
      await axios.post(`${API_URL}/api/cards`, {
        word_text: selectedWord.surface,
        reading: selectedWord.reading,
        lemma: selectedWord.dictionary_form,
        definition: selectedWord.definition, // On utilise la vraie def !
        sentence_context: contextSentence
      });
      alert("Mot sauvegardé avec sa définition !");
    } catch (error) {
      console.error(error);
      alert("Erreur lors de la sauvegarde.");
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto min-h-screen bg-slate-50">
      <header className="mb-8 border-b pb-4">
        <h1 className="text-3xl font-extrabold text-slate-800">日本語 Reader</h1>
        <p className="text-slate-500 italic">Analysez, lisez et apprenez en contexte.</p>
      </header>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Colonne Gauche : Saisie et Lecture */}
        <div className="md:col-span-2 space-y-4">
          <textarea 
            className="w-full p-4 border rounded-xl shadow-sm focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
            rows="6"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Collez votre texte japonais ici..."
          />
	  <button 
	  onClick={analyzeText}
	  disabled={isAnalyzing}
	  className="w-full bg-indigo-600 text-white font-bold py-3 rounded-xl hover:bg-indigo-700 transition shadow-lg"
	  >
	  {isAnalyzing ? "Analyse en cours..." : "Analyser le texte"}
	  </button>  

          <div className="bg-white p-8 rounded-2xl shadow-sm border leading-[3rem] text-2xl min-h-[300px] text-slate-700">
            {tokens.length === 0 && <p className="text-slate-300 italic text-lg text-center mt-10">Le texte analysé apparaîtra ici...</p>}
	   {tokens.map((token, index) => {
	  //  Définition des couleurs selon le statut
	  let statusClass = "hover:bg-gray-200"; // Par défaut
	  if (token.status === "new") {
		  statusClass = "bg-blue-100 border-b-2 border-blue-300";
	  } else if (token.status === "learning") {
		  statusClass = "bg-yellow-100 border-b-2 border-yellow-400";
	  } else if (token.status === "mastered") {
		  statusClass = "text-gray-700"; // Pas de fond pour les mots connus
	  }
	return (
		<span 
		key={index}
		onClick={() => handleWordClick(token, index)}
		className={`cursor-pointer transition-all px-0.5 mx-0.5 rounded ${statusClass} ${
			selectedWord === token ? 'ring-2 ring-indigo-500 bg-indigo-100' : ''
		}`}
		>
		{token.surface}
		</span>
	);
	})}
	  </div>
        </div>

        {/* Colonne Droite : Détails et Contexte */}
	  <div className="flex flex-col gap-2 mt-4">
	  <button 
	  onClick={saveWord}
	  className="w-full bg-emerald-500 text-white py-2 rounded-lg font-bold hover:bg-emerald-600"
	  >
	  Apprendre (SRS)
	  </button>
	  
	  <button 
	  onClick={async () => {
		  await axios.post(`${API_URL}/api/cards/mark-known`, {
			  word_text: selectedWord.surface,
			  reading: selectedWord.reading,
			  lemma: selectedWord.dictionary_form,
			  definition: selectedWord.definition,
			  sentence_context: contextSentence
		  });
		  analyzeText(); // Rafraîchir les couleurs du texte
	  }}
	  className="w-full bg-slate-200 text-slate-700 py-2 rounded-lg font-medium hover:bg-slate-300"
	  >
	  Je connais déjà
	  </button>
	  </div>

	  <div className="md:col-span-1">
          {selectedWord ? (
            <div className="bg-white p-6 rounded-2xl shadow-md border sticky top-6 space-y-4">
              <h2 className="text-4xl font-bold text-slate-800">{selectedWord.surface}</h2>
              <div className="space-y-1">
                <p className="text-indigo-600 font-medium">Reading: {selectedWord.reading}</p>
                <p className="text-slate-400 text-sm italic">POS: {selectedWord.part_of_speech[0]}</p>
              </div>
              
              <div className="pt-4 border-t">
                <h3 className="text-xs uppercase font-bold text-slate-400 mb-2 tracking-widest">Phrase de contexte</h3>
                <p className="text-sm bg-slate-50 p-3 rounded-lg border-l-4 border-indigo-400 italic text-slate-600">
                  "{contextSentence}"
                </p>
              </div>

              <button 
                onClick={saveWord}
                className="w-full mt-4 bg-emerald-500 text-white py-2 rounded-lg font-bold hover:bg-emerald-600 transition"
              >
                Sauvegarder pour révision
              </button>
            </div>
          ) : (
            <div className="h-full border-2 border-dashed border-slate-200 rounded-2xl flex items-center justify-center p-6 text-center text-slate-400 italic text-sm">
              Cliquez sur un mot pour voir ses détails et sa phrase source.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Reader;
