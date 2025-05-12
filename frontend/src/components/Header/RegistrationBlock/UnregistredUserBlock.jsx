import React from "react";
import Button from "../../Button/Button";
import "./UnregistredUserBlock.css";
import Modal from "../../Modal/Modal";
import RegistrationForm from "../../Forms/RegistrationForm/RegistrationForm";
import LoginForm from "../../Forms/LoginForm/LoginForm";

export default function UnregistredUserBlock() {
  const [isModalOpen, setModalOpen] = React.useState(false);
  const [modalType, setModalType] = React.useState("");

  const closeModal = () => {
    setModalOpen(false);
  };

  return (
    <section className="header-button-container">
      <Button
        className="header-button"
        onClick={() => {
          setModalOpen(true);
          setModalType("registration");
        }}
      >
        Зарегистрироваться
      </Button>
      <Button
        className="header-button"
        onClick={() => {
          setModalOpen(true);
          setModalType("login");
        }}
      >
        Войти
      </Button>
      <Modal open={isModalOpen}>
        <div className="modal-content">
          {modalType === "registration" && (
            <RegistrationForm closeModal={closeModal} />
          )}
          {modalType === "login" && <LoginForm closeModal={closeModal} />}
        </div>
      </Modal>
    </section>
  );
}
