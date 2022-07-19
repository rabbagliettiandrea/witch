from invoke import Collection, Program

from witch import __version__ as VERSION
from .tasks import dev, prod, utils, db, aws

namespace = Collection()
namespace.add_collection(prod)
namespace.add_collection(dev)
namespace.add_collection(db)
namespace.add_collection(utils)
namespace.add_collection(aws)
namespace.add_task(prod.shell)
namespace.add_task(prod.exec)

program = Program(namespace=namespace, version=VERSION)
