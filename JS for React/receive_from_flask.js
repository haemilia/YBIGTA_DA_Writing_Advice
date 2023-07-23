import React, { useState } from 'react'; // React 앱에서 Flask의 /api/send-data 엔드포인트를 호출하고 POS tagging 결과를 가져오는 코드
import axios from 'axios';

const App = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [posTags, setPosTags] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const dataToSend = { title, content };
      const response = await axios.post('/api/send_data', dataToSend);
      console.log('Data sent to Flask:', response.data);

      // Flask에서 받아온 POS tagging 결과를 posTags 상태에 저장
      setPosTags(response.data.pos_tags);
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

      <div>
        <h2>POS Tagging Result</h2>
        <ul>
          {posTags.map((tag, index) => (
            <li key={index}>
              Word: {tag.word}, Tag: {tag.tag}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;