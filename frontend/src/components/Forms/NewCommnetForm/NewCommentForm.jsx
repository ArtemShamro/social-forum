import React, { use } from "react";
import Button from "../../Button/Button";
import classes from "./NewCommentForm.module.css";
import { useState } from "react";
import { CreateComment } from "../../../api/comments";

export default function NewCommentForm({ postId }) {
  const [comment, setComment] = useState("");

  return (
    <section>
      <form className={classes.form_input}>
        <textarea
          type="text"
          placeholder="New Comment"
          value={comment}
          onChange={(event) => setComment(event.target.value)}
          rows={5}
        />
        <div className={classes.buttonContainer}>
          <Button
            className={classes.submitButton}
            onClick={(e) => {
              e.preventDefault(); // чтобы форма не перезагружала страницу
              CreateComment({ postId, comment }).then(() =>
                window.location.reload()
              );
            }}
          >
            Отправить
          </Button>
        </div>
      </form>
    </section>
  );
}
