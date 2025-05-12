import React from "react";
import PostsSection from "../components/PostsSection";
import IntroSection from "../components/IntroSection";
import RankingsSection from "../components/Rankings/RankingsSection";
import styles from "./MainPage.module.css";

export default function MainPage() {
  return (
    <div className={styles.mainContainer}>
      <div className={styles.introSection}>
        <IntroSection />
      </div>
      <div className={styles.contentContainer}>
        <div className={styles.postsSection}>
          <PostsSection />
        </div>
        <div className={styles.rankingsSection}>
          <RankingsSection />
        </div>
      </div>
    </div>
  );
}
