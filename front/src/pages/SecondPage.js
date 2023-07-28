import React, { useState } from 'react';
import TextInput from '../components/TextInput';
import axios from 'axios';

const SecondPage = ({ category, text, modifiedText, onGoBack, onContinue}) => {
  const [SecondModifiedText, setSecondModifiedText] = useState(modifiedText);

  const handleTextChange = (event) => {
    setSecondModifiedText(event.target.value);
  };

  const handleGoBack = () => {
    onGoBack();
  };
  
  const handleContinue = () => {
    if (SecondModifiedText.trim().length > 0) {
      
      axios.post('http://127.0.0.1:5000/react_to_flask_2', {
        SecondModifiedText: SecondModifiedText, 
      },{
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      .then((response) => {

        console.log(response.data);

        const analysisResult = response.data.analysisResult;
        const analysisResultImages = response.data.analysisResultImages;

        console.log(analysisResult)

        onContinue(SecondModifiedText, analysisResult, analysisResultImages);
      })
      .catch((error) => {
        console.error('Error while sending data to the server:', error);
      });
    } else {
      alert('Please select a category and enter the text.');
    }
  };


  return (
    <div>
      <h2>Category: {category}</h2>
      <h3>Original Text:</h3>
      <div>{text}</div>
      <h3>Modified Text:</h3>
      <TextInput value={SecondModifiedText} onChange={handleTextChange} />
      <button onClick={handleGoBack}>back</button>
      <button onClick={handleContinue}>Continue</button>
    </div>
  );
};

export default SecondPage;
