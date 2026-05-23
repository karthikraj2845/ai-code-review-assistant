import React, { useState } from 'react';
import CodeEditor from './components/CodeEditor';
import ReviewResults from './components/ReviewResults';
import { reviewCode, explainCode, optimizeCode } from './services/api';

function App() {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('javascript');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [reviewResults, setReviewResults] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!code.trim()) {
      setError('Please enter some code to review');
      return;
    }
    setError('');
    setIsLoading(true);
    try {
      // Call the review endpoint
      const results = await reviewCode(code, language);
      setReviewResults(results);
    } catch (err) {
      setError('Failed to submit code for review: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-center text-gray-800 dark:text-gray-100">
            AI Code Review Assistant
          </h1>
          <p className="text-center text-gray-600 dark:text-gray-300 mt-2">
            Get instant feedback on your code with AI-powered analysis
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <CodeEditor 
              code={code} 
              setCode={setCode}
              language={language}
              setLanguage={setLanguage}
              isLoading={isLoading}
              error={error}
              onSubmit={handleSubmit}
            />
          </div>
          <div>
            <ReviewResults 
              reviewResults={reviewResults}
              isLoading={isLoading}
              error={error}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;