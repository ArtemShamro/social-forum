import React from "react";
import Button from "./Button/Button";
import { useState } from "react";

export default function ButtonSection() {
  const [contentType, setContentType] = useState(null);

  let content1 = "Press The Button";

  console.log("AppComponentRender");

  function handleClick(type) {
    console.log("Button clicked", type);
    setContentType(type);
  }

  let tabContent = null;

  if (contentType) {
    tabContent = <p>{contentType}</p>;
  } else {
    tabContent = <div>Press the Button</div>;
  }
  return (
    <section>
      <Button
        isActive={contentType == "create"}
        onClick={() => handleClick("create")}
      >
        Create
      </Button>
      <Button onClick={() => handleClick("update")}>Update</Button>
      <Button onClick={() => handleClick("delete")}>Delete</Button>
      {contentType ? <p>{contentType}</p> : <div>Press the Button</div>}

      {!contentType ? <div>Press the Button</div> : null}

      {!contentType && <div>Press the Button</div>}
      {contentType && <p>{contentType}</p>}

      {tabContent}
    </section>
  );
}
