import React from 'react';

const ThirdPage = ({ originalText, modifiedText, analysisResult, onContinue, onGoBack }) => {
  const handleGoBack = () => {
    onGoBack();
  };
  
  const handleContinue = () => {
    onContinue();
  };

  return (
    <div>
      <h2>Result</h2>
      <h3>Original Text:</h3>
      <div>{originalText}</div>
      <h3>Modified Text:</h3>
      <div>{modifiedText}</div>
      <h3>Analysis Result:</h3>
      <div>{analysisResult}</div>
      <button onClick={handleGoBack}>back</button>
      <button onClick={handleContinue}>more information</button>
    </div>
  );
};

export default ThirdPage;
