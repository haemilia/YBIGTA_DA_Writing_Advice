import React, { useState } from 'react';
import TextInput from '../components/TextInput';
import axios from 'axios';

const SecondPage = ({ category, text, modifiedText, onContinue }) => {
  const [SecondModifiedText, setSecondModifiedText] = useState(modifiedText);

  const handleTextChange = (event) => {
    setSecondModifiedText(event.target.value);
  };

  const handleContinue = () => {
    if (SecondModifiedText.trim().length > 0) {
      // Axios를 사용하여 Flask 서버로 데이터를 전송합니다.
      // 이때, 실제 서버의 주소로 수정해야 합니다.
      axios.post('http://127.0.0.1:5000/react_to_flask', {
        SecondModifiedText: SecondModifiedText,
      },{
        headers: {
          'Content-Type': 'application/json' // JSON 형식으로 데이터 전송 설정
        }
      })
      
      .then((response) => {

        console.log(response.data);

        // 서버로부터 처리된 텍스트를 전달받습니다.
        const analysisResult = response.data.analysisResult;

        console.log(analysisResult)

        // 다음 페이지로 이동하며, 처리된 텍스트도 함께 전달합니다.
        onContinue(analysisResult, SecondModifiedText);
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
      <button onClick={handleContinue}>Continue</button>
    </div>
  );
};

export default SecondPage;
