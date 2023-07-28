import React from 'react';

const TextInput = ({ value, onChange }) => {
  return (
    <div>
      <textarea rows="10" cols="50" value={value} onChange={onChange} />
    </div>
  );
};

export default TextInput;
