import React, { useState } from 'react';
import FirstPage from './pages/FirstPage';
import SecondPage from './pages/SecondPage';
import ThirdPage from './pages/ThirdPage';
import FourthPage from './pages/FourthPage';

const App = () => {
  const [currentPage, setCurrentPage] = useState('first');
  const [previousPage, setPreviousPage] = useState('first');
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [text, setText] = useState('');
  const [modifiedText, setModifiedText] = useState('');
  const [analysisResult, setAnalysisResult] = useState('');
  const [analysisResultImages, setAnalysisResultImages] = useState(null);

  const handleContinueToSecondPage = (selectedCategory, text, FirstModifiedText) => {
    setSelectedCategory(selectedCategory);
    setText(text);
    setModifiedText(FirstModifiedText);
    setCurrentPage('second');
  }; 

  const handleContinueToThirdPage = (SecondModifiedText, analysisResult, analysisResultImages) => {
    setPreviousPage(currentPage)
    setModifiedText(SecondModifiedText);
    setAnalysisResult(analysisResult);
    setAnalysisResultImages(analysisResultImages);
    setCurrentPage('third');
  };

  const handleContinueToFourthPage = () => {
    setPreviousPage(currentPage)
    setCurrentPage('fourth');
  };

  const handleGoBack = () => {
    setCurrentPage(previousPage);
  };

  const handleReset = () => {
    setCurrentPage('first');
    setPreviousPage(null);
    setSelectedCategory(null);
    setText('');
    setModifiedText('');
    setAnalysisResult('');
    setAnalysisResultImages(null);
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'first':
        return (
          <FirstPage 
            onContinue={handleContinueToSecondPage}
          />
        );
      case 'second':
        return (
          <SecondPage
            category={selectedCategory}
            text={text}
            modifiedText={modifiedText}
            onGoBack={handleGoBack}
            onContinue={handleContinueToThirdPage}
          />
        );
      case 'third':
        return (
          <ThirdPage
            originalText={text}
            modifiedText={modifiedText}
            analysisResult={analysisResult}
            onGoBack={handleGoBack}
            onContinue={handleContinueToFourthPage}
          />
        );
      case 'fourth':
        return (
          <FourthPage
            analysisResultImages = {analysisResultImages}
            onGoBack={handleGoBack}
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
