import React from "react";
// import React from 'react';
import { Card } from "antd";
// const App = () => (
//   <Card title="Card title" variant="borderless" style={{ width: 300 }}>
//     <p>Card content</p>
//     <p>Card content</p>
//     <p>Card content</p>
//   </Card>
// );

// export default App;
export default function Post({ title, description }) {
  const number = 1;
  const now = new Date();

  return (
    <Card
      title={"Название:" + title}
      variant="borderless"
      style={{ width: 300 }}
    >
      <p>Номер Поста: {title}</p>
      <p>OwnerID: {now.toLocaleDateString()}</p>
      <p>Description: {description}</p>
    </Card>
    // <div style={{ border: "2px solid white", padding: "10px", margin: "10px" }}>
    //   <ul>
    //     <li>Номер Поста: {title}</li>
    //     <li>OwnerID: {now.toLocaleDateString()}</li>
    //     <li>Title: {now.toLocaleDateString()}</li>
    //     <li>Description: {description}</li>
    //   </ul>
    // </div>
  );
}
