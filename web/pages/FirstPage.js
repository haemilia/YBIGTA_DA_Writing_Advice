// src/pages/FirstPage.js
import React, { useState } from 'react';
import axios from 'axios';
import CategorySelection from '../components/CategorySelection';
import TextInput from '../components/TextInput';

const FirstPage = ({ onContinue }) => {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [text, setText] = useState('');

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
  };

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  const handleContinue = () => {
    if (selectedCategory && text.trim().length > 0) {
      // Axios를 사용하여 Flask 서버로 데이터를 전송합니다.
      // 이때, 실제 서버의 주소로 수정해야 합니다.
      axios.post('http://127.0.0.1:5000/react_to_flask', {
        category: selectedCategory,
        text: text,
      },{
        headers: {
          'Content-Type': 'application/json' // JSON 형식으로 데이터 전송 설정
        }
      })
      
      .then((response) => {
        // 서버로부터 처리된 텍스트를 전달받습니다.
        const modifiedText = response.data.modifiedText;

        // 다음 페이지로 이동하며, 처리된 텍스트도 함께 전달합니다.
        onContinue(selectedCategory, text, modifiedText);
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
      <h2>Select a category:</h2>
      <CategorySelection onChange={handleCategoryChange} />
      <TextInput value={text} onChange={handleTextChange} />
      <button onClick={handleContinue}>Continue</button>
    </div>
  );
};

export default FirstPage;
