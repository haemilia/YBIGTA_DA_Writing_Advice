import React, { useState, useEffect } from 'react';
import FirstPage from './pages/FirstPage';
import SecondPage from './pages/SecondPage';
import ThirdPage from './pages/ThirdPage';

const App = () => {
  const [currentPage, setCurrentPage] = useState('first');
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [text, setText] = useState('');
  const [modifiedText, setModifiedText] = useState('');
  const [analysisResult, setAnalysisResult] = useState('');

  const handleContinueToSecondPage = (selectedCategory, text, FirstModifiedText) => {
    setSelectedCategory(selectedCategory);
    setText(text);
    setModifiedText(FirstModifiedText);
    setCurrentPage('second');
  }; 

  useEffect(() => {
    console.log(modifiedText);
  }, [modifiedText])

  const handleContinueToThirdPage = (SecondModifiedText, analysisResult) => {
    setModifiedText(SecondModifiedText);
    setAnalysisResult(analysisResult);
    setCurrentPage('third');
  };

  const handleReset = () => {
    setCurrentPage('first');
    setSelectedCategory(null);
    setText('');
    setModifiedText('');
    setAnalysisResult('');
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'first':
        return <FirstPage onContinue={handleContinueToSecondPage} />;
      case 'second':
        return (
          <SecondPage
            category={selectedCategory}
            text={text}
            modifiedText={modifiedText}
            onContinue={handleContinueToThirdPage}
          />
        );
      case 'third':
        return (
          <ThirdPage
            originalText={text}
            modifiedText={modifiedText}
            analysisResult={analysisResult}
            onReset={handleReset}
          />
        );
      default:
        return null;
    }
  };

  return <div className="App">{renderPage()}</div>;
};

export default App;
