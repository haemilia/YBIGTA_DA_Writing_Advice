import React from 'react';

const ThirdPage = ({ originalText, modifiedText, analysisResult, onReset }) => {
  const handleReset = () => {
    onReset();
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
      <button onClick={handleReset}>reset</button>
    </div>
  );
};

export default ThirdPage;
