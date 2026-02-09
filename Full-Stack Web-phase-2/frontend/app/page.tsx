import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      {/* Navigation */}
      <nav className="flex items-center justify-between p-6">
        <div className="text-xl font-bold">TaskMaster</div>
        <div className="flex space-x-4">
          <Button variant="outline" asChild>
            <Link href="/login">Login</Link>
          </Button>
          <Button asChild>
            <Link href="/signup">Sign Up</Link>
          </Button>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-1 flex items-center justify-center p-4">
        <div className="max-w-4xl w-full text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Manage Your Tasks <span className="text-blue-600">Effortlessly</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            A secure, full-stack task management application with authentication. 
            Organize your work, boost productivity, and achieve your goals.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Button size="lg" className="px-8 py-6 text-lg" asChild>
              <Link href="/signup">Get Started - It's Free</Link>
            </Button>
            <Button size="lg" variant="outline" className="px-8 py-6 text-lg" asChild>
              <Link href="/login">Login to Your Account</Link>
            </Button>
          </div>
        </div>
      </main>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Powerful Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🔒</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Secure Authentication</h3>
              <p className="text-gray-600">JWT-based authentication with secure password hashing</p>
            </div>
            <div className="text-center p-6">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📋</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Task Management</h3>
              <p className="text-gray-600">Create, update, and organize your tasks efficiently</p>
            </div>
            <div className="text-center p-6">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📱</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Responsive Design</h3>
              <p className="text-gray-600">Works seamlessly on all devices and screen sizes</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 text-center text-gray-600">
        <p>© {new Date().getFullYear()} TaskMaster. All rights reserved.</p>
      </footer>
    </div>
  );
}