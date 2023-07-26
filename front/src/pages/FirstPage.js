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
      axios.post('http://127.0.0.1:5000/react_to_flask_1', {
        category: selectedCategory,
        text: text,
      },{
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      .then((response) => {

        console.log(response.data);

        const FirstModifiedText = response.data.modifiedText;

        console.log(FirstModifiedText)

        onContinue(selectedCategory, text, FirstModifiedText);
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
