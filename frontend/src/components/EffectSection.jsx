import React from "react";
import Button from "./Button/Button";
import Modal from "./Modal/Modal";
import RegistrationForm from "./Forms/RegistrationForm/RegistrationForm";

export default function EffectSection() {
  const [isModalOpen, setModalOpen] = React.useState(false);

  return (
    <section>
      <h2>Effect Section</h2>

      <Button onClick={() => setModalOpen(true)}>Открыть информацию</Button>
      <Modal open={isModalOpen}>
        <RegistrationForm />
        <Button onClick={() => setModalOpen(false)}>Закрыть</Button>
      </Modal>
    </section>
  );
}
