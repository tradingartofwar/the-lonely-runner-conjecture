// The bounded pilot is one versioned document. A compare-and-swap in D1
// commits each dispatch, lease, evidence link, event and idempotency receipt together.
const { sqliteTable, integer, text } = require("drizzle-orm/sqlite-core");
exports.pilotState = sqliteTable("pilot_state", {
  id: integer("id").primaryKey(),
  revision: integer("revision").notNull(),
  document: text("document").notNull()
});
