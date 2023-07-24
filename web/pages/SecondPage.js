import React, { useState } from 'react';
import TextInput from '../components/TextInput';

const SecondPage = ({ category, text, onContinue }) => {
  const [modifiedText, setModifiedText] = useState(text);

  const handleTextChange = (event) => {
    setModifiedText(event.target.value); // 수정된 텍스트를 상태로 저장합니다.
  };

  const handleContinue = () => {
    onContinue(modifiedText); // 수정된 텍스트를 전달합니다.
  };

  return (
    <div>
      <h2>Category: {category}</h2>
      <h3>Original Text:</h3>
      <div>{text}</div>
      <h3>Modified Text:</h3>
      <TextInput value={modifiedText} onChange={handleTextChange} />
      <button onClick={handleContinue}>Continue</button>
    </div>
  );
};

export default SecondPage;
