import React, { useState } from 'react'; // React에서 title, content 형태의 텍스트 데이터를 입력받고 그 내용을 Flask에 전송
import axios from 'axios';

const App = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const dataToSend = { title, content };
      const response = await axios.post('/api/send_data', dataToSend);
      console.log('Data sent to Flask:', response.data);
    } catch (error) {
      console.error('Error sending data to Flask:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Title:
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </label>
        <br />
        <label>
          Content:
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default App;