<template>
  <header class="topbar">
    <h1>Ventas</h1>
    <nav>
      <RouterLink to="/dashboard">Inicio</RouterLink>
      <RouterLink to="/clientes">Clientes</RouterLink>
      <RouterLink to="/productos">Productos</RouterLink>
      <RouterLink to="/pedidos">Pedidos</RouterLink>
    </nav>
  </header>
  <main class="container">
    <RouterView />
  </main>
</template>
