import React from "react";
import Button from "./Button/Button";

export default function TabSection({ active, onChange }) {
  console.log(active);
  return (
    <section style={{ marginBottom: "1rem" }}>
      <Button isActive={active == "main"} onClick={() => onChange("main")}>
        Main
      </Button>
      <Button isActive={active == "other"} onClick={() => onChange("other")}>
        Other
      </Button>
      <Button isActive={active == "effect"} onClick={() => onChange("effect")}>
        Effect
      </Button>
    </section>
  );
}
