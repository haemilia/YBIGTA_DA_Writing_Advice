import React, { useState } from 'react';
import TextInput from '../components/TextInput';

const SecondPage = ({ category, text, modifiedText, onContinue }) => {
  const [SecondModifiedText, setSecondModifiedText] = useState(modifiedText);

  const handleTextChange = (event) => {
    setSecondModifiedText(event.target.value);
  };

  const handleContinue = () => {
    onContinue(SecondModifiedText);
  };

  return (
    <div>
      <h2>Category: {category}</h2>
      <h3>Original Text:</h3>
      <div>{text}</div>
      <h3>Modified Text:</h3>
      {modifiedText}
      <TextInput value={SecondModifiedText} onChange={handleTextChange} />
      <button onClick={handleContinue}>Continue</button>
    </div>
  );
};

export default SecondPage;
