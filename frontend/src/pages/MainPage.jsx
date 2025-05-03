import React, { useState, useEffect, useContext } from "react";
import PostsSection from "../components/PostsSection";
import IntroSection from "../components/IntroSection";

export default function Posts() {
  return (
    <section>
      <IntroSection />
      <PostsSection />
    </section>
  );
}
