import React, { useState } from 'react';
import TextInput from '../components/TextInput';

const SecondPage = ({ category, text, onContinue }) => {
  const [modifiedText, setModifiedText] = useState(text);

  const handleTextChange = (event) => {
    setModifiedText(event.target.value);
  };

  const handleContinue = () => {
    onContinue(modifiedText);
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
