import React from 'react';

const CategorySelection = ({ onChange }) => {
  const categories = ['논문', '기사', '소설', '시', '에세이'];

  return (
    <div>
      {categories.map((category, index) => (
        <label key={index}>
          <input
            type="radio"
            name="category"
            value={category}
            onChange={() => onChange(category)}
          />
          {category}
        </label>
      ))}
    </div>
  );
};

export default CategorySelection;
