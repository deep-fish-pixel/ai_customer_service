<script lang="ts">
  import { Router, Link, Route } from "svelte5-router";
  import About from "./lib/routes/About.svelte";
  import Space from "./lib/routes/Space.svelte";

  export let url = "";
</script>

  <Router {url}>
    <Route path="/" component={Space} />
    <Route path="/space/:spaceId" component={Space} />
    <Route path="/about" component={About} />
  </Router>


