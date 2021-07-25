<template>
  <v-card>
    <v-card-title>
      {{ name }}
      <v-spacer></v-spacer>
      <a
        class="repo-link"
        v-if="repoLink(link)"
        rel="noopener noreferrer"
        target="_blank"
        :title="link"
        :href="repoLink(link)"
      >
        <v-icon>fab fa-github</v-icon>
      </a>
    </v-card-title>
    <v-card-text>{{ desc }}</v-card-text>
    <v-card-text>
      <template v-if="id">
        <v-icon x-small>fa-fingerprint</v-icon>
        {{ id }}
      </template>
      <v-icon x-small class="ml-2">fa-user</v-icon>
      {{ author }}
    </v-card-text>
    <v-card-actions v-if="showCommand">
      <v-btn block depressed class="btn-copy" @click="copyCommand()">
        {{ text }}
        <v-icon right small>fa-copy</v-icon>
      </v-btn>
      <v-snackbar v-model="snackbar">复制成功！</v-snackbar>
    </v-card-actions>
  </v-card>
</template>

<script>
import copy from "copy-to-clipboard";

export default {
  props: {
    name: String,
    desc: String,
    id: String,
    author: String,
    link: String,
    text: String,
    command: String,
  },
  data() {
    return {
      snackbar: false,
    };
  },
  computed: {
    showCommand() {
      return this.text && this.command;
    },
  },
  methods: {
    repoLink(repo) {
      if (repo) {
        return /^https?:/.test(repo) ? repo : `https://github.com/${repo}`;
      }
      return null;
    },
    copyCommand() {
      copy(this.command, {
        format: "text/plain",
      });
      this.snackbar = true;
    },
  },
};
</script>

<style scoped>
.repo-link {
  text-decoration: none !important;
  display: inline-block;
}
.repo-link:hover i {
  color: #ea5252;
}
</style>
