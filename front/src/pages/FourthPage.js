import React from 'react';

const FourthPage = ({ analysisResultImages, onGoBack, onReset }) => {
  const handleGoBack = () => {
    onGoBack();
  };
  
  const handleReset = () => {
    onReset();
  };

  return (
    <div>
      <h2>Result Images</h2>
      <div>{analysisResultImages}</div>
      <button onClick={handleGoBack}>back</button>
      <button onClick={handleReset}>reset</button>
    </div>
  );
};

export default FourthPage;
