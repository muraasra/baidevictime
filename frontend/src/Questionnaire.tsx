// frontend/src/Questionnaire.tsx
import React, { useEffect, useState } from 'react';

// Définir les types des données API
interface Choice {
  id: number;
  text: string;
  recommended_category?: Category; // Optionnel, peut être undefined
}

interface Question {
  id: number;
  text: string;
  choices: Choice[];
}

interface Category {
  id: number;
  name: string;
}

// Définir les props du composant
interface QuestionnaireProps {
  onCategorySelect: (category: Category) => void;
}

const Questionnaire: React.FC<QuestionnaireProps> = ({ onCategorySelect }) => {
  const [question, setQuestion] = useState<Question | null>(null);

  useEffect(() => {
    // Appel API pour récupérer la première question
    fetch('/api/questions/')
      .then((res) => res.json())
      .then((data: Question[]) => {
        if (data.length > 0) {
          setQuestion(data[0]); // On prend la première question retournée
        }
      })
      .catch((err) => console.error("Erreur API questions:", err));
  }, []);

  if (!question) {
    return <p>Chargement du questionnaire...</p>;
  }

  const handleChoice = (choice: Choice) => {
    // Lorsqu'un choix est sélectionné
    if (choice.recommended_category) {
      onCategorySelect(choice.recommended_category);
    } else {
      // Si on avait plusieurs questions, on pourrait charger la suivante ici
      console.log("Pas de catégorie recommandée pour ce choix.");
    }
  };

  return (
    <div className="questionnaire">
      <h2>{question.text}</h2>
      <ul>
        {question.choices.map((choice) => (
          <li key={choice.id}>
            <button onClick={() => handleChoice(choice)}>
              {choice.text}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Questionnaire;
