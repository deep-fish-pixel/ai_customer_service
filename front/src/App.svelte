<script lang="ts">
  import { Router, Link, Route } from "svelte5-router";
  import About from "./lib/routes/About.svelte";
  import Home from "./lib/routes/Home.svelte";

  export let url = "";
</script>

  <Router {url}>
    <Route path="/" component={Home} />
    <Route path="/space/:spaceId" component={Home} />
    <Route path="/about" component={About} />
  </Router>


