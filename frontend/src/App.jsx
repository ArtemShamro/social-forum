import React, { useState, useEffect, useContext } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header/Header";
import IntroSection from "./components/IntroSection";
import { checkAuth, GetMe } from "./api/user";
import { AuthContext } from "./Context";
import MainPage from "./pages/MainPage";
import PostIdPage from "./pages/PostIdPage";
import ProfilePage from "./pages/ProfilePage";

function App() {
  const [userId, setUserId] = useState(null);
  const [userName, setUserName] = useState("");
  const [tab, setTab] = useState("effect");

  useEffect(() => {
    const verifyUser = async () => {
      const authUser = await checkAuth();
      // console.log("authUser in Effect:", authUser);
      setUserId(authUser);
      if (authUser) {
        const userData = await GetMe();
        setUserName(userData.name);
        // console.log("userName in Effect:", userName);
      }
    };

    verifyUser();
  }, []);

  return (
    <AuthContext.Provider value={[userId, userName]}>
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/post/:id" element={<PostIdPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route element={<MainPage />} />
        </Routes>
      </BrowserRouter>
    </AuthContext.Provider>
  );
}

export default App;

{
  /* <TabSection active={tab} onChange={(current) => setTab(current)} /> */
}
{
  /* {tab == "main" && (
            <>
              <ButtonSection />
            </>
          )}
          {tab == "other" && <FeedbackSection />}
          {tab == "effect" && <EffectSection />} */
}
{
  /* <MainPage />
      <AuthContext.Provider value={[userId, userName]}>
        
        <main>
        </main>
      </AuthContext.Provider> */
}
