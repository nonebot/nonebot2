<template>
  <div class="store">
    <v-app>
      <v-main>
        <v-card>
          <v-toolbar dense flat>
            <v-tabs v-model="tab" centered>
              <v-tab v-for="(name, index) in tabs" :key="index">{{
                name
              }}</v-tab>
            </v-tabs>
          </v-toolbar>
          <v-tabs-items class="sub-item pt-1" v-model="tab">
            <v-tab-item>
              <Adapter></Adapter>
            </v-tab-item>
            <v-tab-item>
              <Plugin></Plugin>
            </v-tab-item>
            <v-tab-item>
              <Bot></Bot>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
      </v-main>
    </v-app>
  </div>
</template>

<script>
import Adapter from "./Adapter.vue";
import Plugin from "./Plugin.vue";
import Bot from "./Bot.vue";

export default {
  name: "Store",
  components: {
    Adapter,
    Plugin,
    Bot
  },
  data() {
    return {
      tab: 1,
      tabs: {
        0: "协议",
        1: "插件",
        2: "机器人"
      }
    };
  },
  computed: {},
  methods: {}
};
</script>

<style>
.v-application--wrap {
  min-height: 0 !important;
}
</style>

<style scoped>
.store {
  margin: 0 -20px;
}
.sub-item {
  padding: 0 10px;
}
</style>
