import React, { useState } from 'react';
import FirstPage from './pages/FirstPage';
import SecondPage from './pages/SecondPage';
import ThirdPage from './pages/ThirdPage';

const App = () => {
  const [currentPage, setCurrentPage] = useState('first');
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [text, setText] = useState('');
  const [modifiedText, setModifiedText] = useState('');
  const [analysisResult, setAnalysisResult] = useState('');

  const handleContinueToSecondPage = (category, inputText) => {
    setSelectedCategory(category);
    setText(inputText);
    setCurrentPage('second');
  };

  const handleContinueToThirdPage = (modifiedText) => {
    setModifiedText(modifiedText);
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
            onContinue={handleContinueToThirdPage}
          />
        );
      case 'third':
        return (
          <ThirdPage
            originalText={text}
            modifiedText={modifiedText}
            analysisResult={analysisResult}
            onReset={handleReset} // 데이터를 리셋하는 함수를 전달합니다.
          />
        );
      default:
        return null;
    }
  };

  return <div className="App">{renderPage()}</div>;
};

export default App;
