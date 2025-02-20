<template>
    <div class="mobile-view">
      <h1>Добро пожаловать в мое приложение!</h1>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MobileView',
  };
  </script>
  
  <style scoped>
  .mobile-view {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    padding: 20px;
    box-sizing: border-box;
    text-align: center;
  }
  
  h1 {
    font-size: 1.5rem;
    color: #333;
  }
  
  @media (min-width: 320px) {
    h1 {
      font-size: 1.2rem;
    }
  }
  
  @media (min-width: 375px) {
    h1 {
      font-size: 1.4rem;
    }
  }
  
  @media (min-width: 390px) {
    h1 {
      font-size: 1.5rem;
    }
  }
  
  @media (min-width: 360px) {
    h1 {
      font-size: 1.3rem;
    }
  }
  </style>