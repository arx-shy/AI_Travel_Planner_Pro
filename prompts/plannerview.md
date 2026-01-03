**Role:** You are the Lead Frontend Architect for "WanderFlow".
**Tech Stack:** Vue 3 (Composition API, `<script setup>`), TypeScript, Tailwind CSS, Pinia.

**Objective:** We are performing a major UI/UX overhaul to fix the "Empty State" issues and "Layout Scrolling" issues identified in our UX audit.

**Instruction:** Please generate/refactor the following 4 files to complete this overhaul in one go.

---

### 1. New Component: `src/components/InspirationDashboard.vue` (The Empty State)

**Goal:** Display this when there is no itinerary generated yet.
**Specs:**

* **Header:** "Where to next?" style welcoming text.
* **Grid:** Responsive grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`).
* **Content:** Mock data for 6 destinations (e.g., Kyoto, Iceland, Paris). Each card needs an image placeholder, title, tag, and a "Plan This" button.
* **Interaction:** Emits `select-destination` event with payload when clicked.
* **Style:** Modern card design with `hover:-translate-y-1` and shadow effects.

### 2. New Component: `src/components/ItinerarySkeleton.vue` (The Loading State)

**Goal:** Show this while AI is generating the itinerary.
**Specs:**

* Use Tailwind `animate-pulse`.
* Layout must mimic the actual `ItineraryItem` (Circle timeline on left, content block on right).
* Render 3 items in a vertical list.

### 3. Refactor Component: `src/components/ItineraryItem.vue` (Visual Polish)

**Goal:** Improve information density and visual hierarchy.
**Changes:**

* **Collapsible Notes:** If the `notes` prop text is longer than 100 characters, truncate it with `line-clamp-2` and show a "Read more/Show less" button.
* **Visuals:** Connect items with a vertical dashed line on the left (Timeline style).
* **Tags:** If specific keywords (like "Warning", "Tips") appear, highlight them subtly.

### 4. Main Layout Refactor: `src/views/PlannerView.vue` (The Layout Fix)

**Goal:** Implement the "Fixed Sidebar + Independent Scroll" layout.
**Changes:**

* **Container:** strictly `h-screen overflow-hidden flex flex-col`.
* **Main Content Area:** Use a Grid or Flex.
  * **Left Column (Form):** Hidden on mobile. On Desktop (`lg`), it must be `w-[350px]`, `h-full`, `overflow-y-auto`, and `border-r`.
  * **Right Column (Content):** `flex-1`, `h-full`, `overflow-y-auto`, `bg-gray-50`.
* **Logic Integration:**
  * Use `v-if="isLoading"` to show `<ItinerarySkeleton />`.
  * Use `v-else-if="!itinerary"` to show `<InspirationDashboard @select-destination="handleSelect" />`.
  * Use `v-else` to show the map and existing list.

---

**Output Requirement:**
Please provide the complete, copy-paste ready code for these 4 files. Use comments to explain key changes.
