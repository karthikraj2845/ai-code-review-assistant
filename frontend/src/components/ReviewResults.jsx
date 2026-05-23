import React from 'react';

const ReviewResults = ({ reviewResults, isLoading, error }) => {
  if (isLoading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-gray-100">
          Review Results
        </h2>
        <div className="flex items-center justify-center py-12">
          <div className="flex space-x-3">
            <div className="w-3 h-3 bg-blue-600 rounded-full animate-pulse"></div>
            <div className="w-3 h-3 bg-blue-600 rounded-full animate-pulse animate-[delay-0.2s]"></div>
            <div className="w-3 h-3 bg-blue-600 rounded-full animate-pulse animate-[delay-0.4s]"></div>
          </div>
          <p className="text-gray-600 dark:text-gray-300 ml-4">Analyzing code...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-gray-100">
          Error
        </h2>
        <div className="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 rounded-md px-4 py-3">
          {error}
        </div>
      </div>
    );
  }

  if (!reviewResults) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-gray-100">
          Review Results
        </h2>
        <p className="text-gray-600 dark:text-gray-300 text-center py-12">
          Submit code to see review results here
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 space-y-6">
      <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-gray-100">
        Review Results
      </h2>
      
      {/* Bug Detection */}
      <div>
        <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-100">
          Bug Detection
        </h3>
        {reviewResults.bugs.length > 0 ? (
          <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
            {reviewResults.bugs.map((bug, index) => (
              <li key={index}>{bug}</li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-600 dark:text-gray-300">No bugs detected.</p>
        )}
      </div>
      
      {/* Optimization Suggestions */}
      <div>
        <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-100">
          Optimization Suggestions
        </h3>
        {reviewResults.optimizations.length > 0 ? (
          <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
            {reviewResults.optimizations.map((opt, index) => (
              <li key={index}>{opt}</li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-600 dark:text-gray-300">No optimization suggestions.</p>
        )}
      </div>
      
      {/* Code Explanation */}
      <div>
        <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-100">
          Code Explanation
        </h3>
        <p className="text-gray-700 dark:text-gray-300">{reviewResults.explanation}</p>
      </div>
      
      {/* Best Practices */}
      <div>
        <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-100">
          Best Practices
        </h3>
        {reviewResults.best_practices.length > 0 ? (
          <ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300">
            {reviewResults.best_practices.map((practice, index) => (
              <li key={index}>{practice}</li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-600 dark:text-gray-300">No best practice recommendations.</p>
        )}
      </div>
      
      {/* Complexity Feedback */}
      <div>
        <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-100">
          Complexity Feedback
        </h3>
        <p className="text-gray-700 dark:text-gray-300">{reviewResults.complexity_feedback}</p>
      </div>
      
      {/* Copy Button */}
      <div className="flex justify-end">
        <button
          onClick={(e) => {
            navigator.clipboard.writeText(JSON.stringify(reviewResults, null, 2));
            alert('Results copied to clipboard!');
          }}
          className="px-4 py-2 bg-gray-600 text-white font-medium rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 transition"
        >
          Copy Results
        </button>
      </div>
    </div>
  );
};

export default ReviewResults;